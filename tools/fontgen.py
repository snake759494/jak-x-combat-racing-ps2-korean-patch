"""한글 음절 글리프(24x32 셀, 4bpp 인덱스: 0=진함..7=옅음, 9=투명)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import FONTS as ROOT, FONTFILE as FONT
SIZE = 27          # 글자 크기(px)
SS = 4             # 슈퍼샘플링
OX, OY = 1, 2      # 셀 안 기준 위치(원본 한자 글리프 위치에 맞춤)
CW, CH = 24, 32

_font = {}
def font(path=FONT, size=SIZE):
    k = (path, size)
    if k not in _font:
        _font[k] = ImageFont.truetype(path, size * SS)
    return _font[k]

def coverage(ch, path=FONT, size=SIZE):
    # 세로 26px 크기로 그린 뒤 가로를 23px 안으로 줄여 셀(24x32)을 채운다(라틴 대문자 높이에 맞춤)
    f = font(path, size)
    WW = 28
    im = Image.new('L', (WW * SS, CH * SS), 0)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), '한', font=f)
    w = d.textbbox((0, 0), ch, font=f)
    x = (WW * SS - (w[2] - w[0])) // 2 - w[0]
    y = OY * SS - bb[1]
    d.text((x, y), ch, font=f, fill=255)
    im = im.resize((CW * SS - 4, CH * SS), Image.LANCZOS)
    full = Image.new('L', (CW * SS, CH * SS), 0); full.paste(im, (2, 0))
    a = np.asarray(full, np.float32).reshape(CH, SS, CW, SS).mean(axis=(1, 3)) / 255.0
    return np.clip(a, 0, 1)

def to_index(cov):
    idx = np.full(cov.shape, 9, np.uint8)
    m = cov > 0.07
    lv = np.clip(np.round((1.0 - cov) * 7.0), 0, 7).astype(np.uint8)
    idx[m] = lv[m]
    return idx

def glyph(ch, path=FONT, size=SIZE):
    return to_index(coverage(ch, path, size))

if __name__ == '__main__':
    import sys
    text = sys.argv[1]; out = sys.argv[2]
    rows = []
    for fp in sys.argv[3:]:
        g = [glyph(c, os.path.join(ROOT, fp)) for c in text]
        rows.append(np.concatenate(g, axis=1))
    a = np.concatenate(rows, axis=0)
    img = np.where(a == 9, 230, a * 20).astype(np.uint8)
    Image.fromarray(img).resize((img.shape[1] * 3, img.shape[0] * 3), Image.NEAREST).save(out)


