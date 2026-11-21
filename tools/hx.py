import sys
p = sys.argv[1]; off = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
n = int(sys.argv[3], 0) if len(sys.argv) > 3 else 512
d = open(p, 'rb').read()[off:off + n]
for i in range(0, len(d), 16):
    c = d[i:i + 16]
    print(f'{off + i:08x}  {c.hex(" "):48s}  {"".join(chr(b) if 32 <= b < 127 else "." for b in c)}')
