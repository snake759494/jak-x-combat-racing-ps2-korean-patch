"""원본 ISO 해시를 확인하고 릴리즈 xdelta를 적용한 뒤 결과 해시를 확인한다.

usage: python tools/apply_release.py --xdelta xdelta3.exe --source 원본.iso --patch 패치.xdelta --output 결과.iso
"""
import argparse, hashlib, json, os, subprocess, sys
R = os.path.join(os.path.dirname(__file__), '..')
m = json.load(open(os.path.join(R, 'release_manifest.json'), encoding='utf8'))
ap = argparse.ArgumentParser()
for a in ('--xdelta', '--source', '--patch', '--output'):
    ap.add_argument(a, required=True)
a = ap.parse_args()

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while b := f.read(1 << 24):
            h.update(b)
    return h.hexdigest()

f = m['files'][0]
if os.path.exists(a.output):
    sys.exit('출력 파일이 이미 있습니다: ' + a.output)
print('원본 확인 중...')
if sha256(a.source) != f['source_sha256']:
    sys.exit('원본 ISO의 SHA-256이 다릅니다. 적용을 중단합니다.')
if sha256(a.patch) != f['asset_sha256']:
    sys.exit('xdelta 파일의 SHA-256이 다릅니다: ' + a.patch)
subprocess.run([a.xdelta, '-d', '-s', a.source, a.patch, a.output], check=True)
if sha256(a.output) != f['output_sha256']:
    sys.exit('결과 파일의 SHA-256이 다릅니다: ' + a.output)
print('완료:', a.output)
