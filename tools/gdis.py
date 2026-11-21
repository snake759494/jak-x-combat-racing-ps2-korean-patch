"""GOAL v5 ?ㅻ툕?앺듃(DGO ?대?) 硫붿씤 ?멸렇癒쇳듃 ?붿뒪?댁뀍釉? ?몄옄: obj?뚯씪 [異쒕젰]"""
import sys, struct
from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS64, CS_MODE_LITTLE_ENDIAN

def segs(d):
    hl = struct.unpack_from('<I', d, 4)[0]
    out = []
    for i in range(3):
        lo, do, ds, ls = struct.unpack_from('<4I', d, 0x50 + 16 * i)
        out.append((lo, ls, hl + do, ds))
    return hl, out

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read()
    hl, sg = segs(d)
    md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS64 + CS_MODE_LITTLE_ENDIAN)
    out = open(sys.argv[2], 'w') if len(sys.argv) > 2 else sys.stdout
    for si, (lo, ls, do, ds) in enumerate(sg):
        out.write(f'== seg{si} file {do:#x} size {ds:#x}\n')
        code = d[do:do + ds]
        for i in range(0, len(code) - 3, 4):
            w = code[i:i + 4]
            ins = list(md.disasm(w, i))
            t = f'{ins[0].mnemonic} {ins[0].op_str}' if ins else f'.word {struct.unpack("<I", w)[0]:#010x}'
            out.write(f'{i:06x}: {w[::-1].hex()}  {t}\n')


