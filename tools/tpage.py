"""Jak X tpage(gamefont) 픽셀 <-> GS VRAM 변환. gsmem.py(간츠 패치에서 가져옴) 사용."""
import struct, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gsmem

B = 0x80

def seg0(d):
    ptr = struct.unpack_from('<I', d, B + 0x1c)[0]
    size = struct.unpack_from('<I', d, B + 0x20)[0] * 4
    return B + ptr, size

_pg = None
def page_index():
    """PSMCT32 폭128(bw=2) 전송, 128x32(=2페이지) 묶음의 워드 -> VRAM 워드주소."""
    global _pg
    if _pg is None:
        _pg = np.array([gsmem.addr32(0, 2, n % 128, n // 128) // 4 for n in range(4096)], np.int64)
    return _pg

def to_vram(raw):
    w = np.frombuffer(raw + b'\0' * (-len(raw) % 16384), '<u4')
    vm = np.zeros(1 << 20, '<u4')
    pi = page_index()
    for p in range(len(w) // 4096):
        vm[p * 4096 + pi] = w[p * 4096:(p + 1) * 4096]
    return vm

def from_vram(vm, size):
    pi = page_index()
    n = (size + 16383) // 16384
    w = np.zeros(n * 4096, '<u4')
    for p in range(n):
        w[p * 4096:(p + 1) * 4096] = vm[p * 4096 + pi]
    return w.tobytes()[:size]

_i4 = {}
def idx4(bp, bw, w, h):
    k = (bp, bw, w, h)
    if k not in _i4:
        _i4[k] = np.array([[gsmem.addr4(bp, bw, x, y) for x in range(w)] for y in range(h)], np.int64)
    return _i4[k]

def read4(vm, bp, bw, w, h):
    v = vm.view(np.uint8)
    a = idx4(bp, bw, w, h)
    b = v[a >> 1]
    return np.where(a & 1, b >> 4, b & 15).astype(np.uint8)

def write4(vm, bp, bw, img):
    v = vm.view(np.uint8)
    h, w = img.shape
    a = idx4(bp, bw, w, h)
    flat_a = a.ravel(); flat_v = img.ravel().astype(np.uint8) & 15
    byte = flat_a >> 1
    hi = (flat_a & 1) == 1
    cur = v[byte]
    v[byte[hi]] = (v[byte[hi]] & 0x0f) | (flat_v[hi] << 4)
    v[byte[~hi]] = (v[byte[~hi]] & 0xf0) | flat_v[~hi]

TEX = {  # name: (dest, bw, w, h)
    'font.12hi': (0, 2, 128, 512), 'font.12lo': (128, 2, 128, 512),
    'font.24hi': (256, 4, 256, 1024), 'font.24hi2': (768, 4, 256, 1024),
    'font.24lo': (1280, 4, 256, 1024), 'font.24lo2': (1792, 4, 256, 1024),
}

if __name__ == '__main__':
    from PIL import Image
    d = open(sys.argv[1], 'rb').read()
    o, s = seg0(d)
    vm = to_vram(d[o:o + s])
    os.makedirs(sys.argv[2], exist_ok=True)
    for n, (bp, bw, w, h) in TEX.items():
        img = read4(vm, bp, bw, w, h)
        Image.fromarray((img * 17).astype(np.uint8)).save(os.path.join(sys.argv[2], n + '.png'))
        print(n, img.max())
