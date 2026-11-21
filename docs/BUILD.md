# 재빌드

## 준비물

- 원본 ISO `Jak X - Combat Racing (USA) (En,Fr,De,Es,It,Pt,Ru) (v2.00).iso` (해시는 README)
- `NanumSquareNeo-eHv.ttf`
- Python 3.13, `pip install pillow numpy capstone zstandard`
- xdelta3 (배포 파일을 만들 때만)

원본 ISO와 글꼴은 저장소 폴더 또는 그 **상위 폴더**에 두면 자동으로 찾습니다. 다른 곳이면 환경변수 `JAKX_BASE`(작업 폴더), `JAKX_ISO`(원본 ISO), `JAKX_FONTS`(글꼴 폴더), `JAKX_OUT`(결과 ISO)로 지정합니다. 작업 파일은 `<작업 폴더>/work/`에 생깁니다.

## 빌드

저장소 폴더에서 실행합니다.

```powershell
python tools/extract.py /TEXT /CGO      # 원본 TEXT·CGO 추출 (work/orig)
python tools/make_src.py                # 원문 목록 translation/src_*.tsv 생성 (배포하지 않음)
python tools/build.py                   # 결과 ISO 생성
```

결과 ISO의 SHA-256을 README의 값과 비교하세요. 같은 원본과 글꼴이면 바이트 단위로 같은 결과가 나옵니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s '<원본.iso>' '<결과.iso>' Jak_X_Combat_Racing_PS2_KO_v1.0.xdelta
```

## 번역 수정

- `translation/ko_common.tsv`, `ko_subtit.tsv`: `텍스트 ID(16진)<TAB>한국어`. 같은 ID의 원문은 `translation/src_*.tsv`에서 봅니다.
- `\n`은 줄바꿈, `<XX>`는 특수 바이트(버튼·국기 아이콘 등)입니다. `~`로 시작하는 마크업(`~Y`, `~Z`, `~22L`, `~+26H` 등은 버튼 아이콘 그리기)과 `~D`·`{`는 원문과 같게 둡니다.
- 원문과 같은 줄은 번역하지 않은 것으로 보고 원본 레코드를 그대로 씁니다.
- 한글 음절은 글꼴 칸 수(592) 안에 들어야 합니다. 넘으면 빌드가 멈추고 드문 음절 목록을 보여 줍니다. `python tools/syl_fix.py extract`로 허용 음절 밖 글자를 쓴 줄을 뽑을 수 있습니다.

## 에뮬레이터 확인

`tools/emu.py`는 PCSX2 휴대용 사본(`<작업 폴더>/emu/pcsx2/`, `portable.ini` 포함, 또는 `JAKX_PCSX2`)을 **보이지 않는 별도 데스크톱**에서 실행하고, 창 메시지로 키를 보내고, PCSX2 스크린샷 단축키(F8)로 화면을 저장합니다. PCSX2 단축키 설정에 `Screenshot = Keyboard/F8`, `SaveStateToSlot = Keyboard/F1`이 있어야 합니다. 키 배치: ✕=K, ○=L, △=I, □=J, START=Enter.

```powershell
python tools/nav.py boot                  # 부팅 → 프로필 생성 화면 → 세이브스테이트
python tools/nav.py run "x w2 L w7 @menu"  # 키 입력, w초 대기, @이름 캡처 (work/qa/)
```
