"""한글패치 빌드: 번역(translation/*.tsv) -> 폰트(tpage-12) + TXT -> 패치 ISO.

번역 파일 형식: id(16진)\t한국어 (원문 마크업 그대로, 줄바꿈은 \\ 문자 그대로)
"""
import os, sys, struct, shutil, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from iso import listing, SEC
import dgo, tpage, fontgen, txtbuild
from jtext import parse

from paths import BASE as ROOT, ISO, OUT, ORIG, TR, WORK, FONTFILE
PAGES = [('font.24hi', 1), ('font.24lo2', 2), ('font.24hi2', 3)]

def is_hangul(c):
    return 0xAC00 <= ord(c) <= 0xD7A3

def _read_tsv(p):
    out = {}
    for ln in open(p, encoding='utf-8-sig'):
        ln = ln.rstrip('\r\n')
        if not ln or ln.startswith('#') or '\t' not in ln:
            continue
        k, v = ln.split('\t', 1)
        out[int(k, 16)] = v
    return out

def load_tr(name):
    """translation/ko_<name>.tsv 가 있으면 사용(없으면 parts/ko_<name>_*.tsv 병합).
    원문(src)과 같은 줄은 번역 안 된 것으로 보고 제외(원본 레코드 유지)."""
    import glob
    base = name.split('.')[0]
    p = os.path.join(TR, 'ko_%s.tsv' % base)
    out = {}
    if os.path.exists(p):
        out = _read_tsv(p)
    else:
        for q in sorted(glob.glob(os.path.join(TR, 'parts', 'ko_%s_*.tsv' % base))):
            out.update(_read_tsv(q))
    src = _read_tsv(os.path.join(TR, 'src_%s.tsv' % base)) if os.path.exists(os.path.join(TR, 'src_%s.tsv' % base)) else {}
    return {k: v for k, v in out.items() if src.get(k) != v}

def collect_syllables(trs):
    freq = {}
    for tr in trs:
        for v in tr.values():
            for c in v:
                if is_hangul(c):
                    freq[c] = freq.get(c, 0) + 1
    syl = sorted(freq, key=lambda c: (-freq[c], c))
    return syl, freq

import re
_TOK = re.compile(r'\\n|<([0-9A-F]{2})>|.', re.S)

def encode(s, cmap):
    out = bytearray()
    for m in _TOK.finditer(s):
        t = m.group(0)
        if t == '\\n':
            out.append(0x5c)
        elif m.group(1):
            out.append(int(m.group(1), 16))
        elif is_hangul(t):
            out += cmap[t]
        elif t in ("'", '’'):
            out.append(0x12)
        elif ord(t) < 0x80:
            out.append(ord(t))
        else:
            raise ValueError('지원 안 되는 문자 %r in %r' % (t, s))
    return bytes(out)

AVOID = {0x20, 0x5c, 0x7e}             # 공백/줄바꿈/마크업 바이트는 2번째 바이트로 쓰지 않음
FLAG3 = set(range(0x7e, 0xb7))          # 페이지3 국기·아이콘 칸(원본 유지)

_used3 = None
def used3():
    """원본 페이지3(font.24hi2)에서 그림이 있는 칸의 코드(국기·대문자 라틴 사본 등) — 보존."""
    global _used3
    if _used3 is None:
        dec = dgo.unzlb(open(os.path.join(ORIG, 'CGO', 'GAME.CGO'), 'rb').read())
        d = next(dec[o2:o2 + s2] for n2, o2, s2 in dgo.split_dgo(dec) if n2 == 'tpage-12')
        o, s = tpage.seg0(d)
        img = tpage.read4(tpage.to_vram(bytes(d[o:o + s])), *tpage.TEX['font.24hi2'])
        _used3 = set()
        for code in range(0x10, 0x100):
            r, c = divmod(code - 6, 10)
            if (img[r * 32:r * 32 + 32, c * 24 + 1:c * 24 + 25] < 8).sum() > 3:
                _used3.add(code)
    return _used3

def slots():
    """(페이지, 코드) 목록. 글리프 칸 번호 = 코드 - 6."""
    out = []
    u3 = used3()
    for page in (1, 2, 3):
        for code in range(0x10, 0x100):
            if code in AVOID or (page == 3 and (code in FLAG3 or code in u3)):
                continue
            out.append((page, code))
    return out

def build_font(syl, sl):
    """tpage-12 의 한글 페이지에 음절 글리프를 그린 새 tpage 바이트 반환(나머지 칸은 원본 유지)."""
    dec = dgo.unzlb(open(os.path.join(ORIG, 'CGO', 'GAME.CGO'), 'rb').read())
    d = next(bytearray(dec[o2:o2 + s2]) for n2, o2, s2 in dgo.split_dgo(dec) if n2 == 'tpage-12')
    o, s = tpage.seg0(d)
    vm = tpage.to_vram(bytes(d[o:o + s]))
    for name, page in PAGES:
        bp, bw, w, h = tpage.TEX[name]
        img = tpage.read4(vm, bp, bw, w, h).copy()
        for k, ch in enumerate(syl):
            pg, code = sl[k]
            if pg != page:
                continue
            r, c = divmod(code - 6, 10)
            img[r * 32:r * 32 + 32, c * 24 + 1:c * 24 + 25] = fontgen.glyph(ch, FONTFILE)
        tpage.write4(vm, bp, bw, img)
    d[o:o + s] = tpage.from_vram(vm, s)
    return bytes(d)

LANGNAME = {0x12: '영어', 0x13: '프랑스어', 0x14: '독일어', 0x15: '스페인어', 0x16: '이탈리아어',
            0x17: '러시아어', 0x18: '일본어', 0x209: '영어', 0x10ae: '포르투갈어'}

def lang_entries(ents, cmap):
    """언어 이름: 국기 마크업(마지막 ~+26H 까지)은 두고 이름만 한국어로."""
    out = {}
    for tid, s in ents:
        if tid in LANGNAME:
            i = s.rfind(b'~+26H')
            pre = s[:i + 5] + b'  ' if i >= 0 else b''
            out[tid] = pre + encode(LANGNAME[tid], cmap)
    return out

def patch_cgo(name, new_tpage):
    raw = open(os.path.join(ORIG, 'CGO', name), 'rb').read()
    dec = bytearray(dgo.unzlb(raw))
    for n, off, sz in dgo.split_dgo(dec):
        if n == 'tpage-12':
            assert sz == len(new_tpage)
            dec[off:off + sz] = new_tpage
        if n == 'font-h':
            # 고정폭(페이지1~3) 글자 전진 폭: 소형 16 -> 13, 대형 32 -> 26 (한글 자간 축소)
            obj = bytearray(dec[off:off + sz])
            for a, b in ((struct.pack('<4f', 12.0, 14.857, 0, 16.0), struct.pack('<4f', 12.0, 14.857, 0, 13.0)),
                         (struct.pack('<4f', 24.0, 29.714, 0, 32.0), struct.pack('<4f', 24.0, 29.714, 0, 26.0))):
                assert obj.count(a) == 1, a
                i = obj.find(a); obj[i:i + 16] = b
            dec[off:off + sz] = obj
        if n == 'font':
            # 소형 폰트에서도 페이지1~3(한글)은 대형 텍스처 템플릿을 쓰도록:
            # lq t2,0xd0(v1)/t3,0xe0/t4,0xf0  ->  0x110/0x120/0x130 (font-work 의 large-font-1..3)
            obj = bytearray(dec[off:off + sz]); cnt = 0
            for a, b in ((0x786a00d0, 0x786a0110), (0x786b00e0, 0x786b0120), (0x786c00f0, 0x786c0130)):
                pa, pb = struct.pack('<I', a), struct.pack('<I', b)
                i = obj.find(pa)
                while i >= 0:
                    if i % 4 == 0:
                        obj[i:i + 4] = pb; cnt += 1
                    i = obj.find(pa, i + 1)
            assert cnt == 12, cnt
            # 효과용 문자열 출력기(GOAL 코드)의 소형 템플릿 복사 ld 0xd0~0xf8 -> 0x110~0x138
            for o_ in (0xd0, 0xd8, 0xe0, 0xe8, 0xf0, 0xf8):
                pa = struct.pack('<I', 0xdc630000 | o_); pb = struct.pack('<I', 0xdc630000 | (o_ + 0x40))
                hits = [i for i in range(0, len(obj) - 3, 4) if obj[i:i + 4] == pa]
                assert len(hits) == 1, (hex(o_), hits)
                obj[hits[0]:hits[0] + 4] = pb
            # 효과용 출력기(일시정지 메뉴 등)는 1/2/3 접두에서 페이지 템플릿을 안 바꿈 -> s3 += 페이지*16 추가
            # 또 원본은 접두 뒤 글리프 바이트를 읽고 포인터를 넘기지 않아 그 바이트를 다시 그림 -> 포인터 +2
            old = [0x9fa601ac, 0x64c60001, 0xafa601ac, 0x24060003, 0x00c3302b, 0x14c00031,
                   0x02e03025, 0x9fa3003c, 0x34630040, 0xafa3003c, 0x9fa301ac, 0x90630000]
            new = [0x9fa601ac,  # lwu   a2, ptr
                   0x2c690004,  # sltiu t1, v1, 4      (접두 1~3 이면 1)
                   0x00c9302d,  # daddu a2, a2, t1
                   0x64c60001,  # daddiu a2, a2, 1
                   0xafa601ac,  # sw    a2, ptr        (접두: +2, 일반: +1)
                   0x11200031,  # beqz  t1, ->0x46dc   (일반 문자)
                   0x00035138,  # dsll  t2, v1, 4      (지연 슬롯)
                   0x026a982d,  # daddu s3, s3, t2     (템플릿 = 현재폰트0 + 페이지*16)
                   0x90c3ffff,  # lbu   v1, -1(a2)     (글리프 바이트)
                   0x9fa9003c, 0x35290040, 0xafa9003c]  # 고정폭 플래그 0x40
            pa = b''.join(struct.pack('<I', w) for w in old)
            hits = [i for i in range(0, len(obj) - 47, 4) if obj[i:i + 48] == pa]
            assert len(hits) == 1, hits
            obj[hits[0]:hits[0] + 48] = b''.join(struct.pack('<I', w) for w in new)
            # 접두 경로가 글리프 표 포인터(sp+0x28)를 누적 저장하고 -0x60 까지 빼는 버그 -> 저장/보정 제거
            old = [0x9fa60028, 0x00033938, 0x00c7302d, 0xafa60028, 0x64c6ffa0]
            new = [0x9fa60028, 0x00033938, 0x00c7302d, 0x00000000, 0x00000000]
            pa = b''.join(struct.pack('<I', w) for w in old)
            hits = [i for i in range(0, len(obj) - 19, 4) if obj[i:i + 20] == pa]
            assert len(hits) == 1, hits
            obj[hits[0]:hits[0] + 20] = b''.join(struct.pack('<I', w) for w in new)
            dec[off:off + sz] = obj
    out, ch = dgo.zlb_rebuild(raw, bytes(dec))
    print(name, 'blocks changed', ch, len(raw), '->', len(out))
    return out

def write_iso(files):
    """files: {'/CGO/GAME.CGO': bytes}. 원본 복사 후 제자리/끝 배치."""
    if not os.path.exists(OUT) or os.path.getsize(OUT) != os.path.getsize(ISO):
        shutil.copyfile(ISO, OUT)
    else:
        # 이전 빌드 흔적 제거: 원본으로부터 변경 대상 영역만 되돌리면 복잡하므로 통째 복사
        shutil.copyfile(ISO, OUT)
    L = {p: (l, s, r) for p, l, s, r in listing(ISO)}
    starts = sorted(l for l, s, r in L.values())
    end = max(l + (s + SEC - 1) // SEC for l, s, r in L.values())
    total = os.path.getsize(ISO) // SEC
    with open(OUT, 'r+b') as f:
        for p, data in files.items():
            l, s, r = L[p]
            nxt = min(x for x in starts if x > l)
            cap = (nxt - l) * SEC
            if len(data) <= cap:
                lba = l
            else:
                lba = end
                end += (len(data) + SEC - 1) // SEC
            f.seek(lba * SEC); f.write(data)
            pad = (-len(data)) % SEC
            f.write(b'\0' * pad)
            f.seek(r + 2); f.write(struct.pack('<I', lba) + struct.pack('>I', lba))
            f.seek(r + 10); f.write(struct.pack('<I', len(data)) + struct.pack('>I', len(data)))
            print(p, 'lba', lba, 'size', len(data), '(in place)' if lba == l else '(moved)')
        newtotal = max(total, end)
        f.seek(newtotal * SEC - 1); f.write(b'\0') if f.seek(0, 2) < newtotal * SEC else None
        f.seek(16 * SEC + 80); f.write(struct.pack('<I', newtotal) + struct.pack('>I', newtotal))

def main():
    tr_c = load_tr('common')
    tr_s = {} if os.environ.get('NOSUB') else load_tr('subtit')
    for k in LANGNAME:
        tr_c.pop(k, None)
    syl, freq = collect_syllables([tr_c, tr_s, {k: v for k, v in LANGNAME.items()}])
    sl = slots()
    print('음절 수', len(syl), '/ 칸', len(sl))
    if len(syl) > len(sl):
        rare = sorted(syl, key=lambda c: freq[c])[:len(syl) - len(sl)]
        raise SystemExit('음절 초과 %d: %s' % (len(syl), ''.join(rare)))
    cmap = {c: bytes(sl[k]) for k, c in enumerate(syl)}
    files = {}
    for fn, tr in (('0COMMON.TXT', tr_c), ('0SUBTIT.TXT', tr_s)):
        o = open(os.path.join(ORIG, 'TEXT', fn), 'rb').read()
        info, ents = parse(o)
        langs = lang_entries(ents, cmap) if fn == '0COMMON.TXT' else {}
        new = []; expect = []
        for tid, s in ents:
            if tid in langs:
                new.append((tid, langs[tid])); expect.append((tid, langs[tid]))
            elif tid in tr:
                e = encode(tr[tid], cmap)
                new.append((tid, e)); expect.append((tid, e))
            else:
                new.append((tid, ('raw',))); expect.append((tid, s))
        for lang in range(12):
            b = txtbuild.build(o, new, lang)
            txtbuild.roundtrip_check(b, expect)
            files['/TEXT/%d%s' % (lang, fn[1:])] = b
        print(fn, len(o), '->', len(b))
    tp = build_font(syl, sl)
    for c in ('GAME.CGO', 'ART.CGO'):
        files['/CGO/' + c] = patch_cgo(c, tp)
    write_iso(files)
    json.dump(syl, open(os.path.join(WORK, 'syllables.json'), 'w', encoding='utf-8'), ensure_ascii=False)

if __name__ == '__main__':
    main()



