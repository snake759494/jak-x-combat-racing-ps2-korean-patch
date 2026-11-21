"""ISO9660 간단 리더: 파일 목록(경로, 시작 LBA, 크기, 디렉터리 레코드 위치)."""
import struct, sys

SEC = 2048

def read_dir(f, lba, size, path, out):
    f.seek(lba * SEC)
    data = f.read(size)
    pos = 0
    while pos < len(data):
        ln = data[pos]
        if ln == 0:
            pos = (pos // SEC + 1) * SEC
            continue
        rec = data[pos:pos + ln]
        elba = struct.unpack_from('<I', rec, 2)[0]
        esz = struct.unpack_from('<I', rec, 10)[0]
        flags = rec[25]
        nl = rec[32]
        name = rec[33:33 + nl]
        if name not in (b'\x00', b'\x01'):
            nm = name.decode('ascii', 'replace').split(';')[0]
            full = path + '/' + nm
            recpos = lba * SEC + pos
            if flags & 2:
                read_dir(f, elba, esz, full, out)
            else:
                out.append((full, elba, esz, recpos))
        pos += ln

def listing(iso):
    with open(iso, 'rb') as f:
        f.seek(16 * SEC)
        pvd = f.read(SEC)
        root = pvd[156:156 + 34]
        lba = struct.unpack_from('<I', root, 2)[0]
        size = struct.unpack_from('<I', root, 10)[0]
        out = []
        read_dir(f, lba, size, '', out)
        return out

if __name__ == '__main__':
    for p, l, s, r in sorted(listing(sys.argv[1]), key=lambda x: x[1]):
        print(f'{l:8d} {s:11d} {p}')
