# 잭 X: 컴뱃 레이싱 (PS2) 한글패치

PS2 북미판 **Jak X: Combat Racing (SCUS-97429, v2.00)**용 비공식 한국어 패치입니다. 메뉴·옵션·안내문·차량/무기/캐릭터 설명 등 게임 텍스트 **1,715항목**과 컷신 자막 **1,433문장**을 한국어로 바꿨습니다. 게임에 남아 있던 일본어 글꼴 칸에 한글 **584자**를 그려 넣고, 일부 화면(레이스 일시정지 메뉴 등)의 글자 출력 코드를 고쳐 한글이 나오게 했습니다. 현재 배포판은 **v1.0 (2026-11-21)**입니다.

[패치 다운로드](https://github.com/snake759494/jak-x-combat-racing-ps2-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [번역 지침·용어집](docs/STYLE.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 **Jak_X_Combat_Racing_PS2_KO_v1.0.xdelta 하나**입니다. 저장소에는 제작 도구·문서·한국어 번역만 공개합니다. 원본·완성 디스크 이미지, 추출한 게임 데이터, 영어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『잭 X: 컴뱃 레이싱』은 너티 독이 개발하고 소니 컴퓨터 엔터테인먼트가 2005년에 낸 「잭 앤 덱스터」 시리즈의 카 컴뱃 레이싱 게임입니다. 독이 든 술을 마신 잭 일행이 해독제를 얻기 위해 크라스 시티 그랑프리에 나서는 이야기로, 무기를 단 차량으로 서킷 레이스·데스 레이스·프리즈 랠리 등 여러 이벤트를 치릅니다.

이 패치는 **북미판 v2.00 DVD ISO (2,048바이트 섹터)**에만 적용합니다. 파일 이름보다 아래 크기와 해시가 일치하는지가 중요합니다.

| 항목 | 값 |
| --- | --- |
| 게임 ID | SCUS-97429 |
| 원본 형식 | 수정되지 않은 북미판 v2.00 DVD ISO (En,Fr,De,Es,It,Pt,Ru) |
| 원본 ISO 크기 | 4,662,296,576 B |
| **원본 ISO MD5** | `05ed20ea58cf6c410314d1fd1905c002` |
| 원본 ISO SHA-256 | `0e106c1f974bc85e8a04b90d1ca67ab06733a8ca4ca00f6110797a7538df37f8` |
| xdelta 파일 크기 | 7,203,760 B |
| xdelta SHA-256 | `24ca17ca3d54b6f3e6ec705f2328ce3918f3d6938dad597e6e97de3a2525a89f` |
| 결과 ISO 크기 | 4,662,296,576 B (원본과 같음) |
| 결과 ISO MD5 | `e89420b5a69a63028c922be47b298383` |
| 결과 ISO SHA-256 | `9081e589ef065a082683912db4ec3bc08c980411cb7538397c1702e1f8ae91eb` |

SHA-1은 [release_manifest.json](release_manifest.json)에 있습니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\Jak X - Combat Racing (USA) (En,Fr,De,Es,It,Pt,Ru) (v2.00).iso'
```

위 표와 다르면 적용을 중단하세요. CHD·CSO 등으로 변환한 이미지에는 적용할 수 없습니다.

### xdelta UI 사용

1. 릴리즈에서 `Jak_X_Combat_Racing_PS2_KO_v1.0.xdelta`를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 `.iso`를 선택합니다.
4. **Output File**에는 새 파일 이름(예: `Jak X - Combat Racing (USA) (Korean).iso`)을 지정합니다.

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다(`-e -0 -S none -A`).

### 명령줄 사용

```powershell
.\xdelta3.exe -d -s '.\Jak X - Combat Racing (USA) (En,Fr,De,Es,It,Pt,Ru) (v2.00).iso' '.\Jak_X_Combat_Racing_PS2_KO_v1.0.xdelta' '.\Jak X - Combat Racing (USA) (Korean).iso'
```

해시를 자동으로 검사하는 도구도 있습니다(Python 3, xdelta3 필요).

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source '.\원본.iso' --patch '.\Jak_X_Combat_Racing_PS2_KO_v1.0.xdelta' --output '.\Jak X (Korean).iso'
```

### 게임 설정

- 게임 안 언어는 무엇을 골라도 한국어로 나옵니다.
- **컷신 자막은 기본으로 꺼져 있습니다.** 메인 메뉴 → 옵션 → 게임 옵션 → **자막**을 「켜기」로 바꾸세요.
- **16:9 와이드**: 옵션 → 화면 옵션 → **화면 형태**를 「16x9」로 바꾸고, PCSX2의 화면 비율(Aspect Ratio)도 「Widescreen (16:9)」로 맞추세요. 별도 와이드 패치는 필요 없습니다.
- 북미판이므로 **✕ 버튼이 결정, △ 버튼이 뒤로**입니다. 세이브 데이터 형식은 바꾸지 않았습니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 게임 텍스트 | 메뉴·옵션·메모리 카드 메시지·튜토리얼 안내·레이스 HUD·결과·차량/무기/캐릭터 설명·비밀 상점 등 **1,715항목** (`TEXT/*COMMON.TXT`) |
| 컷신 자막 | 스토리 컷신 자막 **1,433문장** (`TEXT/*SUBTIT.TXT`) |
| 글꼴 | 게임 글꼴 텍스처(`tpage-12`)의 일본어 칸에 한글 **584자**(나눔스퀘어네오 Heavy) |
| 코드 | 효과 문자열 출력기(일시정지 메뉴 등)의 다국어 글자 처리 수정, 한글 자간 조정, 소형 글꼴의 한글 페이지 연결 |

12개 언어 슬롯을 모두 한국어로 채웠습니다. 바뀐 파일은 원래 자리에 넣거나 디스크 끝에 덧붙이고 디렉터리만 고쳤습니다. 자세한 내용은 [docs/TECHNICAL.md](docs/TECHNICAL.md)를 참고하세요.

### 번역 원칙

- 기계 번역 없이 영어 원문과 문맥을 보고 직접 번역했습니다.
- 인명·지명·이벤트 이름은 [용어집](docs/STYLE.md)으로 통일했습니다. 예: 잭, 닥스터, 키라, 크라스 시티, 데스 레이스, 다크 에코.
- 메뉴는 명사형, 안내문은 「~하세요」, 대사는 캐릭터 말투를 살렸습니다.
- 글꼴 칸이 592개뿐이라 드문 음절을 쓰는 표현은 흔한 음절로 다시 다듬었습니다.

### 번역하지 않은 것

- 음성(영어)
- JAK X 타이틀 로고, 3D 배경에 그려진 간판·광고
- 개발용으로 남은 문자열(`asdf`, `Test Menu`, "Do Not Translate" 표시 문장)
- PAL/NTSC, LAN, CPU 같은 표기

## 알려진 한계

- PCSX2 v2.2.0에서 타이틀, 프로필 생성·저장, 메모리 카드 안내, 메인 메뉴, 옵션 전체, 친선전(화면 모드·이벤트·드라이버·차량 선택), 레이스 HUD, 레이스 일시정지 메뉴, 커스터마이즈, 비밀 상점, 오프닝 컷신 자막, 첫 튜토리얼을 확인했습니다. 스토리 전체 완주와 온라인 화면, 실기에서의 동작은 확인하지 못했습니다.
- 레이스 화면 오른쪽의 「랩」「시간」 라벨은 4:3 화면에서 가장자리에 붙어 보입니다.
- 일본 BIOS로 실행하면 컷신 자막이 나오지 않습니다(원본 영어판도 같음). 북미 BIOS를 쓰세요.
- 글자가 잘리거나 영어가 남은 화면을 발견하면 이슈로 스크린샷과 함께 알려 주세요.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `tools/build.py` | 원본 ISO에서 한글판 ISO를 빌드(텍스트 재구성, 글꼴 생성, 코드 패치, CGO 재압축, ISO 기록) |
| `tools/` | `iso.py` ISO9660 읽기, `extract.py` 파일 추출, `dgo.py`·`lzoc.py` oZlB(LZO1X) 해제·압축, `jtext.py`·`txtbuild.py` 게임 텍스트 읽기·쓰기, `tpage.py`·`gsmem.py` 글꼴 텍스처와 GS 메모리 배치, `fontgen.py` 한글 글리프, `make_src.py` 원문 목록, `syl_fix.py` 음절 수 관리, `emu.py`·`nav.py` 에뮬레이터 조작, `gdis.py` 코드 디스어셈블, `apply_release.py` 해시 검사 후 적용 |
| `translation/` | 번역. `ko_common.tsv`(게임 텍스트), `ko_subtit.tsv`(자막) — `텍스트 ID<TAB>한국어` |
| `docs/` | 기술 설명, 재빌드 방법, 번역 지침·용어집, 글꼴 출처 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
