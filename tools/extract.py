"""ISO에서 지정 파일을 work/orig 로 추출. 인자: 경로 접두(예: /TEXT /CGO)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from iso import listing, SEC

from paths import ISO, ORIG

def main(prefixes):
    out = ORIG
    with open(ISO, 'rb') as f:
        for p, l, s, r in listing(ISO):
            if any(p.startswith(x) for x in prefixes):
                d = os.path.join(out, p.lstrip('/'))
                os.makedirs(os.path.dirname(d), exist_ok=True)
                f.seek(l * SEC)
                open(d, 'wb').write(f.read(s))
                print(p, s)

if __name__ == '__main__':
    main(sys.argv[1:])
