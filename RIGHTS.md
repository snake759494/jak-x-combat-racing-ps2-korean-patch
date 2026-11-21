# 권리 및 외부 자료

이 저장소는 비공식 한국어 패치의 제작 소스·번역·검증 자료를 공개하기 위한 것입니다. 『Jak X: Combat Racing』(PS2, Naughty Dog / Sony Computer Entertainment)과 그 텍스트·이미지·영상·음성·실행 코드, 등장 캐릭터의 권리는 원 권리자에게 있습니다.

배포하지 않는 것은 원본 게임, 패치를 적용한 게임, 게임에서 추출한 데이터·그래픽·영상·음성, 영어 원문입니다. 릴리즈에는 원본 디스크 이미지가 있어야만 쓸 수 있는 차분 파일(xdelta)만 첨부합니다. 번역(`translation/ko_*.tsv`)은 원문 대신 게임 안 텍스트 ID로만 연결되며, 원문은 빌드할 때 사용자의 원본 ISO에서 읽습니다(`tools/make_src.py`).

저장소를 공개했다고 해서 모든 파일에 같은 오픈소스 라이선스를 부여한다는 뜻은 아닙니다. 자체 제작 코드와 번역 전체에 대한 포괄 라이선스는 따로 지정하지 않았습니다.

게임 안 한글은 나눔스퀘어네오(© NAVER Corp., SIL Open Font License 1.1, 전문은 `LICENSES/NanumSquareNeo-OFL-1.1.txt`)로 그렸습니다. 글꼴 파일 자체는 저장소에 넣지 않았습니다(`docs/FONT_CREDITS.md` 참고).

`tools/gsmem.py`의 GS 메모리 배치 표는 공개된 PS2 GS 메모리 구조를 옮긴 것입니다. xdelta, PCSX2, Python 라이브러리(Pillow, NumPy, capstone, zstandard) 등 외부 도구는 각 프로젝트의 라이선스를 따르며, 바이너리는 재배포하지 않습니다. 게임 코드를 디스어셈블한 결과물은 넣지 않았고, 해석한 내용과 바꾼 명령만 `docs/TECHNICAL.md`에 정리했습니다. 텍스트·글꼴 형식 해석에는 공개된 OpenGOAL 프로젝트의 분석 자료를 참고했습니다.
