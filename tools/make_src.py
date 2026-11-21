"""번역 원문 생성: translation/src_common.tsv, src_subtit.tsv (id\t원문). 줄바꿈은 \\n 로 표기."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from jtext import parse

from paths import ORIG, TR

def clean(b):
    s = b.decode('latin-1')
    s = re.sub(r'~\+(\d)V(.)~-\1V', r'\2', s)
    s = s.replace('\x12', "'").replace('\\', '\\n')
    out = []
    for c in s:
        o = ord(c)
        if 32 <= o < 127 or c == '\n':
            out.append(c)
        else:
            out.append('<%02X>' % o)
    return ''.join(out)

def main():
    os.makedirs(TR, exist_ok=True)
    for fn, name in (('0COMMON.TXT', 'common'), ('0SUBTIT.TXT', 'subtit')):
        d = open(os.path.join(ORIG, 'TEXT', fn), 'rb').read()
        _, ents = parse(d)
        with open(os.path.join(TR, 'src_%s.tsv' % name), 'w', encoding='utf-8') as f:
            for tid, s in ents:
                f.write('%04x\t%s\n' % (tid, clean(s)))

if __name__ == '__main__':
    main()
