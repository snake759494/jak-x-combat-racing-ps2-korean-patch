"""음절 예산 관리: 허용 음절표 생성 + 허용 밖 음절을 쓴 줄 추출 / 수정본 반영."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(__file__))
import build

ROOT = build.ROOT; TR = build.TR
os.makedirs(os.path.join(TR, 'parts'), exist_ok=True)
LIMIT = 585   # 글리프 칸 592(페이지3 원본 그림 칸·0x20/0x5C/0x7E 제외)
NAMES = ('잭 닥스터 키라 사모스 시그 톤 애슐린 테스 페커 크루 자이먼 레이저 미조 클리버 레인 베저 백작 오스모 블리츠 '
         '태린 시브 그림 리릴 오닌 심 빈 크라스 시티 헤이븐 스파거스 컴뱃 레이싱 그랑프리 데스 레이스 서킷 프리즈 랠리 '
         '타임 트라이얼 데스매치 캡처 아티팩트 러시 터보 대시 스포츠 헌트 수집전 셔틀 예선 에코 다크 라이트 그린 프리커서 '
         '오브 메탈 헤드 크림존 가드 약탈자 황무지 차고 마르 피스메이커 스캐터 건 벌컨 퓨리 블래스터 프로필 메모리 카드 '
         '랩 순위표 컵 클래스 시즌 이벤트 브론즈 실버 골드 비밀 치트')

def parts(name):
    import glob
    return [os.path.join(TR, 'ko_%s.tsv' % name)]

def main(mode):
    c = build.load_tr('common'); s = build.load_tr('subtit')
    syl, freq = build.collect_syllables([c, s])
    must = {ch for ch in NAMES if build.is_hangul(ch)}
    allowed = list(must) + [x for x in syl if x not in must]
    allowed = set(allowed[:LIMIT])
    json.dump(sorted(allowed), open(os.path.join(TR, 'allowed.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    bad = []
    for name, tr in (('common', c), ('subtit', s)):
        src = build._read_tsv(os.path.join(TR, 'src_%s.tsv' % name))
        for k, v in tr.items():
            b = sorted({ch for ch in v if build.is_hangul(ch) and ch not in allowed})
            if b:
                bad.append((name, k, src.get(k, ''), v, ''.join(b)))
    print('음절', len(syl), '허용', len(allowed), '수정 필요 줄', len(bad))
    if mode == 'extract':
        n = 3; k = (len(bad) + n - 1) // n
        for i in range(n):
            with open(os.path.join(TR, 'parts', 'fix_%d.tsv' % i), 'w', encoding='utf-8') as f:
                for name, kk, en, ko, b in bad[i * k:(i + 1) * k]:
                    f.write('%s:%04x\t%s\t%s\t%s\n' % (name, kk, en, ko, b))

def apply():
    """parts/fixed_*.tsv (key\t새번역) 를 각 ko 조각에 반영."""
    import glob
    fixes = {}
    for p in glob.glob(os.path.join(TR, 'parts', 'fixed_*.tsv')):
        for ln in open(p, encoding='utf-8-sig'):
            ln = ln.rstrip('\r\n')
            if '\t' in ln:
                k, v = ln.split('\t', 1)
                fixes[k] = v
    n = 0
    for name in ('common', 'subtit'):
        for p in parts(name):
            L = open(p, encoding='utf-8-sig').read().splitlines()
            for i, ln in enumerate(L):
                if '\t' not in ln:
                    print('탭 없음', p, i, repr(ln)); continue
                k, v = ln.split('\t', 1)
                key = '%s:%04x' % (name, int(k, 16))
                if key in fixes:
                    L[i] = k + '\t' + fixes[key]; n += 1
            open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('반영', n)

if __name__ == '__main__':
    if sys.argv[1] == 'apply':
        apply()
    else:
        main(sys.argv[1])



