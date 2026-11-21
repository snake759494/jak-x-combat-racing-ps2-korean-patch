"""Jak X game-text-info (TEXT/*.TXT) 파서/빌더.

구조(데이터 기준 0x80, 포인터는 데이터 시작 기준 오프셋):
  +0  type tag(ffffffff)  +4 length(엔트리 수)  +8 language  +12 group-name
  +16 dic-index  +20 dic-data  +24 text(id,index 쌍)  +28 text-data
문자열 = 사전 조각 번호 목록(1바이트 길이/플래그) -> 조각(1바이트 길이 + 바이트) 이어붙임.
"""
import struct, sys, json

B = 0x80

def u32(d, o):
    return struct.unpack_from('<I', d, o)[0]

def parse(d):
    hdr = B + 4  # 'basic' 데이터 시작(타입 태그 다음)
    cnt = u32(d, hdr + 0)
    lang = u32(d, hdr + 4)
    gname = u32(d, hdr + 8)
    dic_index = u32(d, hdr + 12)
    dic_data = u32(d, hdr + 16)
    text = u32(d, hdr + 20)
    text_data = u32(d, hdr + 24)
    out = []
    for i in range(cnt):
        tid = u32(d, B + text + i * 8)
        idx = u32(d, B + text + i * 8 + 4)
        p = B + text_data + idx
        b = d[p]; p += 1
        flag = b & 0x80; n = b & 0x7f
        if n == 127:
            while True:
                a = d[p]; p += 1; n += a
                if a != 255:
                    break
        s = bytearray()
        for j in range(n):
            if flag:
                k = d[p + 2 * j] | (d[p + 2 * j + 1] << 8)
            else:
                k = d[p + j]
            dp = B + dic_data + u32(d, B + dic_index + 4 * k)
            ln = d[dp]
            s += d[dp + 1:dp + 1 + ln]
        out.append((tid, bytes(s)))
    info = dict(count=cnt, lang=lang, gname=gname, dic_index=dic_index, dic_data=dic_data,
                text=text, text_data=text_data)
    return info, out

def show(b):
    r = []
    for c in b:
        if 32 <= c < 127 and c != 0x5c:
            r.append(chr(c))
        else:
            r.append('\\x%02x' % c)
    return ''.join(r)

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read()
    info, ents = parse(d)
    print(info)
    for tid, s in ents:
        print('%04x\t%s' % (tid, show(s)))
