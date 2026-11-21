"""LZO1X 압축기(탐욕적 해시 체인). dgo.lzo1x_decompress 와 호환."""

def _lit_run(out, src, s, e, after_match):
    t = e - s
    if t == 0:
        return
    if not out:  # 스트림 시작
        if t <= 238:
            out.append(17 + t)
        else:
            _long_lit(out, t)
    elif t <= 3:
        out[-2] |= t
    elif t <= 18:
        out.append(t - 3)
    else:
        _long_lit(out, t)
    out += src[s:e]

def _long_lit(out, t):
    out.append(0)
    tt = t - 18
    while tt > 255:
        out.append(0); tt -= 255
    out.append(tt)

def _match(out, mlen, moff):
    if mlen <= 8 and moff <= 0x800:
        m = moff - 1
        out.append(((mlen - 1) << 5) | ((m & 7) << 2))
        out.append(m >> 3)
    elif moff <= 0x4000:
        m = moff - 1
        if mlen <= 33:
            out.append(0x20 | (mlen - 2))
        else:
            ml = mlen - 33
            out.append(0x20)
            while ml > 255:
                out.append(0); ml -= 255
            out.append(ml)
        out.append((m << 2) & 0xff); out.append((m >> 6) & 0xff)
    else:
        m = moff - 0x4000
        k = (m & 0x4000) >> 11
        if mlen <= 9:
            out.append(0x10 | k | (mlen - 2))
        else:
            ml = mlen - 9
            out.append(0x10 | k)
            while ml > 255:
                out.append(0); ml -= 255
            out.append(ml)
        out.append((m << 2) & 0xff); out.append((m >> 6) & 0xff)

def compress(src):
    src = bytes(src)
    n = len(src)
    out = bytearray()
    head = {}
    i = 0
    lit = 0
    MAXOFF = 0xbfff
    while i < n - 2:
        key = src[i:i + 3]
        cands = head.get(key)
        best_len = 0; best_off = 0
        if cands:
            tries = 0
            for p in reversed(cands):
                off = i - p
                if off > MAXOFF:
                    break
                l = 3
                mx = min(n - i, 0x800)
                while l < mx and src[p + l] == src[i + l]:
                    l += 1
                # M2(짧은 거리) 우대 없이 단순 최장
                if l > best_len:
                    best_len, best_off = l, off
                    if l >= mx:
                        break
                tries += 1
                if tries >= 16:
                    break
        if best_len >= 3 and not (best_len == 3 and best_off > 0x800):
            _lit_run(out, src, lit, i, True)
            _match(out, best_len, best_off)
            for j in range(i, i + best_len):
                if j + 3 <= n:
                    head.setdefault(src[j:j + 3], []).append(j)
            i += best_len
            lit = i
        else:
            head.setdefault(key, []).append(i)
            i += 1
    _lit_run(out, src, lit, n, True)
    out += b'\x11\x00\x00'
    return bytes(out)

if __name__ == '__main__':
    import sys, os, random
    sys.path.insert(0, os.path.dirname(__file__))
    from dgo import lzo1x_decompress
    d = open(sys.argv[1], 'rb').read()
    tot = 0
    for o in range(0, min(len(d), 0x8000 * int(sys.argv[2])), 0x8000):
        blk = d[o:o + 0x8000]
        c = compress(blk)
        r, _ = lzo1x_decompress(c)
        assert bytes(r) == blk, o
        tot += len(c)
    print('ok', tot)
