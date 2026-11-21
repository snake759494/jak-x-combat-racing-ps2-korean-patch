"""검수용 화면 탐색: 부팅→메인메뉴 세이브(슬롯1), 키 입력 후 캡처 몽타주."""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))
import emu
from PIL import Image

from paths import OUT as ISO, WORK
SP = os.path.join(WORK, 'qa')
os.makedirs(SP, exist_ok=True)

def boot_menu(iso=ISO):
    emu.start(iso); time.sleep(30)
    for i in range(22):
        time.sleep(10); emu.keys('start')
    time.sleep(8)
    emu.keys('x w6 x w4'); emu.key('L', hold=0.4); time.sleep(7); emu.key('K', hold=0.4); time.sleep(9)
    return emu.savestate()

def load():
    emu.key('F3'); time.sleep(4)

def shot(name, crop=True):
    p = os.path.join(SP, name + '.png'); img = emu.shot(p)
    if crop:
        pass
    img.resize((625, 465)).save(p)
    return p

def run(seq):
    """seq: '키들 | 캡처이름' 반복. 예: 'down x w3 @a1 tri w2 @a2'"""
    for t in seq.split():
        if t.startswith('@'):
            shot(t[1:])
        elif t.startswith('w'):
            time.sleep(float(t[1:]))
        else:
            emu.key(emu.ALIAS.get(t, t)); time.sleep(0.6)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'boot':
        print(boot_menu())
    elif cmd == 'load':
        load()
    elif cmd == 'run':
        run(' '.join(sys.argv[2:]))



