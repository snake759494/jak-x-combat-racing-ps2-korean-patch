"""Jak X game-text-info(.TXT) 재구성.

원본의 사전 0..223(문자 변환표, expand-text 용)은 그대로 두고, 그 뒤에 단어 토큰을 추가한다.
문자열 = 토큰 번호 목록(항상 2바이트 번호, 플래그 0x80).
"""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from jtext import parse, u32, B

def tokenize(s):
    """공백 뒤에서 끊어 단어 단위 토큰(최대 255바이트)."""
    toks = []; cur = bytearray()
    for b in s:
        cur.append(b)
        if b == 0x20 or len(cur) >= 255:
            toks.append(bytes(cur)); cur = bytearray()
    if cur:
        toks.append(bytes(cur))
    return toks

def raw_records(d):
    hdr = B + 4
    cnt = u32(d, hdr); text = u32(d, hdr + 20); td = u32(d, hdr + 24)
    out = {}
    for i in range(cnt):
        tid = u32(d, B + text + i * 8); p = B + td + u32(d, B + text + i * 8 + 4)
        q = p; b = d[q]; q += 1; flag = b & 0x80; n = b & 0x7f
        if n == 127:
            while True:
                a = d[q]; q += 1; n += a
                if a != 255:
                    break
        q += n * (2 if flag else 1)
        out[tid] = d[p:q]
    return out

def build(orig, entries, lang=None):
    """orig: 원본 TXT 바이트, entries: [(id, bytes)] (id 오름차순)."""
    hdr = B + 4
    lang = u32(orig, hdr + 4) if lang is None else lang
    di = u32(orig, hdr + 12); dd = u32(orig, hdr + 16)
    base = []
    nd = (dd - di) // 4
    for k in range(nd):
        p = B + dd + u32(orig, B + di + 4 * k)
        base.append(orig[p + 1:p + 1 + orig[p]])
    gname = u32(orig, hdr + 8)
    gstr_len = u32(orig, B + gname + 4)
    gstr = orig[B + gname + 8:B + gname + 8 + gstr_len]

    dic = list(base); index = {}
    for k, v in enumerate(base):
        index.setdefault(v, k)
    entries = sorted(entries)
    tdata = bytearray(); table = []
    raws = raw_records(orig)
    # 한 번만 나오는 토큰이 연달아 있으면 합쳐 사전 항목 수를 줄인다
    from collections import Counter
    cnt = Counter()
    for tid, s in entries:
        if not isinstance(s, tuple):
            cnt.update(tokenize(s))
    def merged(s):
        out = []
        for t in tokenize(s):
            if out and cnt[t] == 1 and cnt.get(out[-1], 1) == 1 and len(out[-1]) + len(t) <= 255 and out[-1] not in index:
                out[-1] = out[-1] + t
            else:
                out.append(t)
        return out
    for tid, s in entries:
        if isinstance(s, tuple):  # ('raw',) : 원본 레코드 그대로
            table.append((tid, len(tdata)))
            tdata += raws[tid]
            continue
        toks = merged(s)
        ids = []
        for t in toks:
            if t not in index:
                index[t] = len(dic); dic.append(t)
            ids.append(index[t])
        table.append((tid, len(tdata)))
        n = len(ids)
        if n < 127:
            tdata.append(0x80 | n)
        else:
            tdata.append(0x80 | 127); r = n - 127
            while r >= 255:
                tdata.append(255); r -= 255
            tdata.append(r)
        for i in ids:
            tdata += struct.pack('<H', i)
    assert len(dic) < 65536
    # 배치: [tag][header 0x20 이후] dic-index, dic-data, text-data, text, 그룹명 string
    data = bytearray(b'\xff\xff\xff\xff')
    data += b'\0' * 0x1c
    def align(n):
        while len(data) % n:
            data.append(0)
    o_di = len(data)
    dd_bytes = bytearray(); offs = []
    for t in dic:
        offs.append(len(dd_bytes)); dd_bytes.append(len(t)); dd_bytes += t
    for o in offs:
        data += struct.pack('<I', o)
    o_dd = len(data); data += dd_bytes; align(4)
    o_td = len(data); data += tdata; align(16)
    o_tx = len(data)
    for tid, off in table:
        data += struct.pack('<II', tid, off)
    align(16)
    o_str = len(data)
    data += b'\xff\xff\xff\xff' + struct.pack('<I', len(gstr)) + gstr + b'\0'
    size = len(data) - 1  # 원본처럼 실제 사용 길이
    align(16)
    # 헤더: 포인터는 데이터 시작(type tag 위치) 기준 오프셋
    struct.pack_into('<IIIIIII', data, 4, len(entries), lang, o_str + 4, o_di, o_dd, o_tx, o_td)
    # 링크 블록
    def varoff(v):
        assert v % 4 == 0
        if v < 0x100 and v != 0 or v == 0:
            if v == 0:
                return bytes([0])
            return bytes([v])
        if v < 0x10000:
            return bytes([(v & 0xff) | 1, v >> 8])
        return bytes([(v & 0xff) | 2, (v >> 8) & 0xff, (v >> 16) & 0xff])
    link = bytearray(struct.pack('<IIII', 0x10, 0, size, 1))
    link += bytes([4, 5, 0])
    link += b'\x80\xed\x15game-text-info\0' + varoff(0) + b'\0'
    link += b'\xc0\x11\x00string\0' + varoff(o_str) + b'\0'
    link += b'\0'
    while len(link) % 16:
        link.append(0)
    # 파일 헤더(0x80)
    h = bytearray(orig[:0x80])
    struct.pack_into('<I', h, 0x0c, 0x80 + len(data))
    struct.pack_into('<I', h, 0x10, len(link))
    return bytes(h + data + link)

def roundtrip_check(new, entries):
    info, ents = parse(new)
    assert sorted(entries) == ents, 'roundtrip mismatch'

if __name__ == '__main__':
    o = open(sys.argv[1], 'rb').read()
    info, ents = parse(o)
    n = build(o, ents)
    roundtrip_check(n, ents)
    print(len(o), len(n))
    open(sys.argv[2], 'wb').write(n)


