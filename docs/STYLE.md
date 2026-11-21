# 젝 X: 컴뱃 레이싱 번역 지침

## 출력 형식
- 입력 파일과 같은 줄 수, 같은 순서: `id<TAB>한국어` (UTF-8). id 는 그대로 복사.
- 한 줄 = 한 항목. 원문 줄바꿈 `\n` 은 그대로 `\n` 두 글자로 둔다(위치는 한국어 문장에 맞게 조정 가능, 개수는 원문과 같게).

## 반드시 보존할 것 (그대로 복사)
- `~` 로 시작하는 모든 제어 마크업: `~Y`, `~Z`, `~]`, `~[`, `~22L`, `~+26H`, `~-12V`, `~1L` 등 및 그 사이 기호(`<`, `>`, `[`, `*`, `#`, `@`, `;`) — 이것은 버튼 아이콘을 그리는 코드다. 예: `~Y~22L<~Z~Y~27L*~Z~Y~1L>~Z~Y~23L[~Z~+26H` 는 ✕버튼 아이콘 한 덩어리. 통째로 복사하고 한국어 어순에 맞게 위치만 옮겨라.
- `<A6>` 처럼 `<16진수2자리>` 표기 = 특수 기호 바이트. 그대로 둔다.
- `~D`, `~S`, `~1K` 같은 서식 지정자, `{`(붙임 공백) — 그대로.
- 고유 영문 표기 유지: START, SELECT, L1, R1, L2, R2, PlayStation, MEMORY CARD (PS2), DNAS, LAN, ID, URL, 숫자, 차량/무기 모델명 중 영문 코드(예: NYFE-Racer 는 번역).
- 따옴표 '’'는 `'` 로.

## 문체
- 메뉴/UI: 간결한 명사형 (예: "Load Profile" → "프로필 불러오기", "Options" → "옵션").
- 안내문: 합쇼체(~합니다/~하십시오) 대신 "~하세요/~합니다" 혼용 금지 → 안내는 "~하세요", 설명은 "~합니다".
- 자막/대사: 캐릭터 말투 살리기. 닥스터는 촐싹대는 반말, 잭은 짧고 단호한 반말. 적들은 거친 반말. 어른/부하 관계는 상황에 맞게.
- 대문자 외침(SWEET!, YOU RULE!)은 짧고 맛깔나게.
- 한 줄 길이: 원문보다 눈에 띄게 길게 쓰지 말 것(화면 폭 제한). 한글 1자 ≈ 영문 2자 폭.

## 글자 수 제한 (매우 중요)
- 게임 폰트에 넣을 수 있는 한글 음절은 **총 592종**뿐이다. 흔한 음절 위주로 쓰고 희귀한 음절(예: 꽤뀌쐐쭤쳬퓌 등, 받침이 복잡한 드문 글자)을 피하라.
- 같은 뜻이면 더 흔한 단어를 고르라. 외래어 표기도 흔한 음절로.

## 용어집 (반드시 통일)
Jak 잭 / Daxter 닥스터 / Keira 키라 / Samos 사모스 / Sig 시그 / Torn 톤 / Ashelin 애슐린 / Tess 테스 / Pecker 페커 / Krew 크루 / Ximon 자이먼 / Razer 레이저 / Mizo 미조 / Kleiver 클리버 / Rayn 레인 / UR-86 UR-86 / Count Veger 베저 백작 / Osmo 오스모 / G.T. Blitz G.T. 블리츠 / Taryn 태린 / Shiv 시브 / Grim 그림 / Lyril 리릴 / Torn 톤 / Ximon 자이먼 / Tess 테스 / Onin 오닌 / Seem 심 / Krew 크루 / Vin 빈
Kras City 크라스 시티 / Haven City 헤이븐 시티 / Spargus 스파거스 / Combat Racing 컴뱃 레이싱 / Kras City Grand Prix 크라스 시티 그랑프리 / Death Race 데스 레이스 / Circuit Race 서킷 레이스 / Freeze Rally 프리즈 랠리 / Time Trial 타임 트라이얼 / Deathmatch 데스매치 / Capture 캡처 / Artifact Race 아티팩트 레이스 / Rush 러시 / Turbo Dash 터보 대시 / Sport Hunt 스포츠 헌트 / Collectathon 수집전 / Shuttle 셔틀 / Qualifier 예선 / Eco 에코 / Dark Eco 다크 에코 / Light Eco 라이트 에코 / Green eco 그린 에코 / Precursor 프리커서 / Precursor Orb 프리커서 오브 / Dark Jak 다크 잭 / Light Jak 라이트 잭 / Metal Heads 메탈 헤드 / Krimzon Guard 크림존 가드 / Marauders 약탈자 / Wastelanders 황무지 사람들 / garage 차고 / Mar 마르 / Mar Memorial / 마르 기념 / Turbo 터보 / Peace Maker 피스메이커 / Scatter gun 스캐터 건 / Vulcan Fury 벌컨 퓨리 / Blaster 블래스터 / Profile 프로필 / Memory card 메모리 카드 / Lap 랩 / Leaderboard 순위표 / Cup 컵 / Class 클래스 / Season 시즌 / Event 이벤트 / Bronze/Silver/Gold 브론즈/실버/골드(메달은 동메달/은메달/금메달 가능) / Secrets 비밀 / Cheats 치트

지명·고유명사 목록에 없는 것은 자연스러운 음역(흔한 음절)으로, 일반명사는 의미를 번역.

## 기타
- `asdf`, `test`, `tem` 같은 개발용 잔재 문자열은 원문 그대로 둔다.
- 영어 이외 언어 이름(Français, Deutsch 등이 마크업으로 된 줄)은 원문 그대로 둔다.
- 원문이 비어 있거나 마크업만 있는 줄은 원문 그대로.
- 절대 외부 번역 도구/웹 사용 금지. 직접 번역.

