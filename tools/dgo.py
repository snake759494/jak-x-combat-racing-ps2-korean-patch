"""Jak X CGO/DGO: oZlB(LZO1X 블록) 해제/재압축 + DGO 오브젝트 분할."""
import struct, sys, os

def lzo1x_decompress(src, ip=0, out=None):
    if out is None:
        out = bytearray()
    n = len(src)

    def copy_match(mpos, cnt):
        if mpos < 0:
            raise ValueError('lzo bad match')
        if mpos + cnt <= len(out):
            out.extend(out[mpos:mpos + cnt])
        else:
            for k in range(cnt):
                out.append(out[mpos + k])

    state = 'start'
    t = 0
    while True:
        if state == 'start':
            t = src[ip]
            if t > 17:
                ip += 1
                t -= 17
                if t < 4:
                    state = 'match_next'
                    continue
                out.extend(src[ip:ip + t]); ip += t
                state = 'first_lit'
                continue
            state = 'loop'
            continue
        if state == 'loop':
            t = src[ip]; ip += 1
            if t >= 16:
                state = 'match'
                continue
            if t == 0:
                while src[ip] == 0:
                    t += 255; ip += 1
                t += 15 + src[ip]; ip += 1
            out.extend(src[ip:ip + t + 3]); ip += t + 3
            state = 'first_lit'
            continue
        if state == 'first_lit':
            t = src[ip]; ip += 1
            if t >= 16:
                state = 'match'
                continue
            mpos = len(out) - (1 + 0x0800) - (t >> 2) - (src[ip] << 2); ip += 1
            copy_match(mpos, 3)
            state = 'match_done'
            continue
        if state == 'match':
            if t >= 64:
                mpos = len(out) - 1 - ((t >> 2) & 7) - (src[ip] << 3); ip += 1
                t = (t >> 5) - 1
                copy_match(mpos, t + 2)
            elif t >= 32:
                t &= 31
                if t == 0:
                    while src[ip] == 0:
                        t += 255; ip += 1
                    t += 31 + src[ip]; ip += 1
                mpos = len(out) - 1 - ((src[ip] | (src[ip + 1] << 8)) >> 2); ip += 2
                copy_match(mpos, t + 2)
            elif t >= 16:
                mpos = len(out) - ((t & 8) << 11)
                t &= 7
                if t == 0:
                    while src[ip] == 0:
                        t += 255; ip += 1
                    t += 7 + src[ip]; ip += 1
                mpos -= (src[ip] | (src[ip + 1] << 8)) >> 2; ip += 2
                if mpos == len(out):
                    return out, ip
                mpos -= 0x4000
                copy_match(mpos, t + 2)
            else:
                mpos = len(out) - 1 - (t >> 2) - (src[ip] << 2); ip += 1
                copy_match(mpos, 2)
            state = 'match_done'
            continue
        if state == 'match_done':
            t = src[ip - 2] & 3
            if t == 0:
                state = 'loop'
                continue
            state = 'match_next'
            continue
        if state == 'match_next':
            out.extend(src[ip:ip + t]); ip += t
            t = src[ip]; ip += 1
            state = 'match'
            continue


def unzlb(data):
    if data[:4] != b'oZlB':
        return bytes(data)
    total = struct.unpack_from('<I', data, 4)[0]
    out = bytearray()
    p = 8
    while len(out) < total:
        p = (p + 3) & ~3
        sz = struct.unpack_from('<I', data, p)[0]; p += 4
        if sz < 0x8000:
            blk, _ = lzo1x_decompress(data[p:p + sz])
            out.extend(blk)
        else:
            out.extend(data[p:p + 0x8000])
            sz = 0x8000
        p += sz
    return bytes(out[:total])


def zlb_chunks(data):
    """원본 oZlB 의 청크(바이트열) 목록. 각 청크는 0x8000 바이트로 풀린다."""
    total = struct.unpack_from('<I', data, 4)[0]
    p = 8; got = 0; out = []
    while got < total:
        p = (p + 3) & ~3
        sz = struct.unpack_from('<I', data, p)[0]; p += 4
        n = sz if sz < 0x8000 else 0x8000
        out.append(bytes(data[p:p + n])); p += n
        got += 0x8000
    return out


def zlb_rebuild(orig, new):
    """바뀐 0x8000 블록만 다시 압축하고 나머지 청크는 원본 그대로 사용."""
    import lzoc
    old = unzlb(orig)
    assert len(old) == len(new)
    chunks = zlb_chunks(orig)
    out = bytearray(b'oZlB' + struct.pack('<I', len(new)))
    changed = 0
    for i, ch in enumerate(chunks):
        a = old[i * 0x8000:(i + 1) * 0x8000]
        b = new[i * 0x8000:(i + 1) * 0x8000]
        if a != b:
            changed += 1
            blk = b + b'\0' * (0x8000 - len(b))
            c = lzoc.compress(blk)
            if len(c) >= 0x8000:
                c = blk
            ch = c
        while len(out) % 4:
            out.append(0)
        out += struct.pack('<I', len(ch) if len(ch) < 0x8000 else 0x8000) + ch
    return bytes(out), changed


def zlb_store(data):
    """무압축 블록(크기 0x8000 표기)으로 oZlB 생성."""
    out = bytearray(b'oZlB' + struct.pack('<I', len(data)))
    for i in range(0, len(data), 0x8000):
        blk = data[i:i + 0x8000]
        blk = blk + b'\0' * (0x8000 - len(blk))
        while len(out) % 4:
            out.append(0)
        out += struct.pack('<I', 0x8000) + blk
    return bytes(out)


def split_dgo(d):
    cnt = struct.unpack_from('<I', d, 0)[0]
    p = 0x40
    objs = []
    for i in range(cnt):
        sz = struct.unpack_from('<I', d, p)[0]
        name = d[p + 4:p + 0x40].split(b'\0')[0].decode()
        objs.append((name, p + 0x40, sz))
        p += 0x40 + sz
        p = (p + 15) & ~15
    return objs

if __name__ == '__main__':
    src = sys.argv[1]; dst = sys.argv[2]
    d = unzlb(open(src, 'rb').read())
    open(dst, 'wb').write(d)
    print(len(d), d[:64])
