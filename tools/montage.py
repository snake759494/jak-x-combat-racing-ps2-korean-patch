import sys
from PIL import Image
out = sys.argv[1]; names = sys.argv[2:]
ims = [Image.open(n) for n in names]
W = sum(i.width for i in ims) + 10 * len(ims); H = max(i.height for i in ims)
c = Image.new('RGB', (W, H), (128,128,128)); x = 0
for i in ims:
    c.paste(i.convert('RGB'), (x, 0)); x += i.width + 10
c.save(out)

