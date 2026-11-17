# 규리네 초밥은 못 참지 (Sushi Rush)

회전초밥 퍼즐 웹 게임 초안입니다. 모바일 세로 화면 기준이며 PC 브라우저에서도 동작합니다.

**플레이:** https://smhotkdg.github.io/sushiRush/

## 규칙
- 아래 보드의 줄을 터치하면 **맨 위 재료 1개**가 주방장에게 넘어갑니다.
- 주방장은 대기열 순서대로 초밥을 하나씩 만들어 레일에 올린 뒤 다음 재료를 조리합니다.
- 주방장이 만든 초밥은 벨트를 돌다가, 그 초밥을 주문한 손님 앞에서 전달됩니다.
- 주문을 다 받은 손님은 떠나고 다음 손님이 옵니다. 모든 주문을 채우면 스테이지 클리어.
- 하단 게이지는 보낸 재료, 조리 중인 재료, 레일 투입을 기다리는 초밥, 레일 위의 초밥을 모두 셉니다. 합계가 최대 용량에 닿는 순간 게임 오버입니다.
- 스테이지 모드의 레일 용량은 처음 10칸으로 시작하고 12개 스테이지마다 1칸씩 늘어납니다. 무한 모드의 레일 용량은 18칸입니다.
- PC: 숫자 키 1~5 로 줄 선택, Esc 로 일시정지.

## 무한 모드
- 재료 줄은 항상 12개 이상 쌓여 있고, 손님 순서에 맞춰 아래에서 계속 이어 붙습니다. 앉아 있는 손님의 재료가 너무 깊이 묻히면 맨 위로 끌어올려 막힘을 막습니다.
- 손님과 재료가 끝없이 이어지고, 손님이 늘수록 재료 종류·주문량·벨트 속도가 올라갑니다. 벨트 속도는 손님 약 100명 부근에서 상한에 도달합니다.
- 주문 말풍선 안의 게이지는 손님의 남은 인내심을 보여 줍니다. 첫 손님에게는 여유를 주고, 응대한 손님이 늘어날수록 새 손님의 대기시간이 완만하게 줄어듭니다. 게이지가 다 닳으면 손님이 떠나며 ♥를 1개 잃습니다. 남은 주문은 나중에 다시 옵니다.
- ♥ 3개를 다 잃거나 벨트가 가득 차면 종료. 점수 = 초밥 10점(+콤보 보너스) + 손님 완료 50점.
- 순위는 모두 Firebase(Firestore)에 저장됩니다. 계정마다 최고 기록 1개만 남고, 전체 TOP 10과 내 순위를 보여 줍니다. 로그인 전에 끝낸 기록은 하루 동안 보관했다가 로그인하면 올립니다.

## 로그인 (카카오 · 네이버 · Google)
설정(톱니바퀴)과 모드 선택 화면에서 로그인합니다. 처음 로그인한 계정은 닉네임을 한 번 정하고, 이후에는 바꿀 수 없습니다(개발자용 화면에서만 초기화).

서버가 없는 정적 사이트라서 세 곳 모두 "로그인 페이지로 이동 → 게임 주소로 돌아옴" 방식이며, 게임 코드에는 공개용 ID만 들어 있습니다. **Client Secret 은 절대 `index.html` 에 넣지 마세요.** `.env` 는 `.gitignore` 로 제외됩니다.

각 개발자 콘솔에 아래 주소를 등록해야 동작합니다.

| 서비스 | 등록 위치 | 값 |
|---|---|---|
| 카카오 | 앱 > 플랫폼 > Web 사이트 도메인 | `https://smhotkdg.github.io` |
| 카카오 | 카카오 로그인 > Redirect URI | `https://smhotkdg.github.io/sushiRush/` |
| 네이버 | 내 애플리케이션 > API 설정 > 서비스 URL | `https://smhotkdg.github.io` |
| 네이버 | 네이버 로그인 Callback URL | `https://smhotkdg.github.io/sushiRush/` |
| Google | OAuth 클라이언트 > 승인된 JavaScript 원본 | `https://smhotkdg.github.io` |
| Google | OAuth 클라이언트 > 승인된 리디렉션 URI | `https://smhotkdg.github.io/sushiRush/` |

- 카카오는 콘솔에서 **Client Secret 이 켜져 있으면** 서버 없이 토큰을 받을 수 없어 로그인되지 않습니다. 서버(예: Firebase Functions)를 붙이면 `AUTH_CONFIG.kakaoTokenUrl` 로 인가 코드를 보내도록 되어 있습니다.
- 네이버는 공식 JavaScript SDK(implicit 방식)를 씁니다. 공개 전에는 등록한 테스트 계정만 로그인됩니다.
- 처음 로그인하면 바로 닉네임을 정하고, Firebase `players` 에 저장됩니다. 닉네임은 전체에서 겹칠 수 없고 바꿀 수 없습니다. 다른 기기에서 같은 계정으로 로그인하면 닉네임과 기록이 이어집니다.

## Firebase
- 프로젝트 `sushirush-3cf7f`, 웹 앱 `SushiRush Web`, Firestore(서울 `asia-northeast3`), 익명 인증 사용. 설정은 `firebase.js`, 규칙은 `firestore.rules`.
- 컬렉션: `players/{pid}`(닉네임), `nicknames/{소문자 닉네임}`(중복 방지), `leaderboard/{pid}`(무한 모드 최고 기록). `pid` 는 `kakao_123` 처럼 로그인 서비스와 계정 ID 를 합친 값입니다.
- 규칙 배포: `firebase deploy --only firestore:rules` 또는 콘솔 > Firestore > 규칙에 붙여 넣고 게시.
- 닉네임을 지우려면 콘솔에서 `players/{pid}` 와 `nicknames/{닉네임}` 문서를 함께 삭제합니다(게임에서는 바꿀 수 없음).
- **한계**: 게임 로그인을 서버에서 검증하지 않으므로, 규칙은 형식·범위·점수 증가·점수 상한만 막습니다. Cloud Functions 로 카카오·네이버·구글 토큰을 검증해 커스텀 토큰을 발급하면 `request.auth.uid == pid` 조건으로 본인만 쓰게 바꿀 수 있습니다.

## 개발자용 화면
설정 > 개발자용, 비밀번호 `2222` (`DEV_PASSWORD`). 게임 기록 초기화, 로그인 기록 초기화, Firebase 연결 확인, 전체 스테이지 열기, 로그인 연동 정보가 있습니다. `DEV_TOOLS` 배열에 `{id, label, desc, danger, run}` 항목을 추가하면 화면에 자동으로 나옵니다. 비밀번호는 공개 코드에 들어 있으므로 보안 장치가 아니라 실수 방지용입니다.

## 타이틀 화면
`assets/title.webp` 한 장을 쓰고, 그림 속 "게임 시작" 버튼과 톱니바퀴 위치에 터치 영역을 얹었습니다. 그림을 바꾸면 `index.html` 의 `ART_W`, `ART_H` 와 `#startHot`, `#gearHot` 의 위치(%)를 맞춰 주세요.

게임 시작 시 `assets/entrance.webp`의 좌우 반쪽이 미닫이문처럼 닫히며 `assets/welcome.mp3`의 환영 음성이 재생됩니다.

타이틀과 모드 선택에서는 `assets/BGM.mp3`에서 만든 `assets/menu-loop.mp3`가 재생됩니다. 첫 재생에는 도입부가 포함되고, 반복할 때는 크로스페이드한 끝에서 5.82초 지점으로 이어집니다. 게임에 들어가면 기존 인게임 BGM으로 전환됩니다.

## 구조
파일 하나(`index.html`)로 되어 있고 빌드가 필요 없습니다.

| 위치 | 내용 |
|---|---|
| `ASSET_URLS`, `TYPES` | 재료·초밥 그림 (기본은 코드 내 SVG) |
| `stageConfig(n)` | 스테이지별 난이도 값 |
| `sfx`, `MEL`, `BASS` | Web Audio로 합성하는 효과음과 배경음 |
| `assets/restaurant/*_blink.webp` | 주방장과 네 손님의 아이들 깜빡임 프레임 |
| `burst`, `ring`, `floatText` | 이펙트(파티클) |

## 이미지 교체
`assets/` 폴더에 PNG 를 넣고 `index.html` 상단 `ASSET_URLS` 에 경로를 적으면 됩니다.

```js
const ASSET_URLS = {
  ing_tuna:   'assets/ing_tuna.png',    // 보드에 쌓이는 재료
  sushi_tuna: 'assets/sushi_tuna.png',  // 벨트·말풍선의 초밥 (비우면 자동 합성)
};
```

키: `tuna`, `egg`, `shrimp`, `salmon`, `cucumber`, `octopus`, `roe`, `eel`
