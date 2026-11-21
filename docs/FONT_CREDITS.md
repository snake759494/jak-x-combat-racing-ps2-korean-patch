# 글꼴 출처

원본 글꼴이 굵은 산세리프라 한글도 가장 굵은 고딕 계열로 맞췄습니다.

| 용도 | 한글 글꼴 |
| --- | --- |
| 게임 글꼴 `tpage-12` (`font.24hi`·`font.24lo2`·`font.24hi2`) 의 한글 584자 | 나눔스퀘어네오 Hv (`NanumSquareNeo-eHv.ttf`) |

- 24×32 칸에 27px 크기로 4배 확대 렌더한 뒤 가로를 23px로 맞춰 줄이고, 원본 글꼴과 같은 4비트 회색 단계(0=진함~7=옅음, 9=투명)로 바꿨습니다(`tools/fontgen.py`).
- 작은 글씨(12px)도 같은 24px 글리프를 축소해 그리는 구조라 별도 비트맵 글꼴은 쓰지 않았습니다.
- 나눔스퀘어네오: © NAVER Corp., SIL Open Font License 1.1 (`LICENSES/NanumSquareNeo-OFL-1.1.txt`)

글꼴 파일은 저장소에 포함하지 않습니다. 재빌드하려면 `NanumSquareNeo-eHv.ttf`를 원본 ISO와 같은 폴더(또는 `JAKX_FONTS`로 지정한 폴더)에 두세요.
