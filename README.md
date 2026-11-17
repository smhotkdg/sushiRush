# 스시 러시 (Sushi Rush)

회전초밥 퍼즐 웹 게임 초안입니다. 모바일 세로 화면 기준이며 PC 브라우저에서도 동작합니다.

**플레이:** https://smhotkdg.github.io/sushiRush/

## 규칙
- 아래 보드의 줄을 터치하면 **맨 위 재료 1개**가 주방장에게 넘어갑니다.
- 주방장이 만든 초밥은 벨트를 돌다가, 그 초밥을 주문한 손님 앞에서 전달됩니다.
- 주문을 다 받은 손님은 떠나고 다음 손님이 옵니다. 모든 주문을 채우면 스테이지 클리어.
- 가운데 바는 벨트 위 초밥 수 / 최대치입니다. 가득 찬 채 3초가 지나면 게임 오버.
- PC: 숫자 키 1~5 로 줄 선택, Esc 로 일시정지.

## 구조
파일 하나(`index.html`)로 되어 있고 빌드가 필요 없습니다.

| 위치 | 내용 |
|---|---|
| `ASSET_URLS`, `TYPES` | 재료·초밥 그림 (기본은 코드 내 SVG) |
| `stageConfig(n)` | 스테이지별 난이도 값 |
| `sfx`, `MEL`, `BASS` | 효과음·배경음 (WebAudio 합성, 음원 파일 없음) |
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
