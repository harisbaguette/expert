# 정의 기준선의 생성과 검사

이 폴더는 실제 전문 에이전트 제품이 아니라 **정의 문서의 정본·생성·검증 도구**다. 문서의 의미 검토는 [기준선 검토](../reviews/material-baseline-review.md), 직무별 범위는 [166개 범위 대장](occupation-scopes.csv)에 있다.

## 정본과 생성물

| 입력 | 생성물 |
|---|---|
| 루트 정의 1의 설명표 + `../materials.md` 대응·세부 표 | 구성 도식 SVG |
| `implementation-guide.md` + `../materials.md` | 루트 정의 2 |
| 루트 정의 1·진행 계획 Markdown | 각각의 HTML, Mermaid SVG와 판본 목록 |
| 정본·그래프·범위 대장·과거 제한 모형 | `verification-result.json` |

`implementation-guide.md`는 루트 정의 2의 템플릿이므로 그 안의 상대 링크는 **생성 결과의 위치**를 기준으로 한다. `archive/`의 예전 내용은 생성 입력이 아니다.

## 실행

Python 표준 라이브러리로 상세 정의와 구성 그림을 만들고 검사한다.

```sh
python3 docs/definition/build_views.py
python3 docs/definition/render_html.py
node docs/definition/visual_check.cjs
python3 docs/definition/verify_definition.py
```

HTML 생성에는 Node.js, Pandoc, Playwright와 그 버전에 맞는 Chromium, Mermaid의 브라우저 스크립트가 필요하다. 모듈을 프로젝트 밖에 설치했다면 다음 환경 변수를 지정한다.

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright \
MERMAID_SCRIPT=/path/to/node_modules/mermaid/dist/mermaid.js \
CHROMIUM_EXECUTABLE=/path/to/chromium \
python3 docs/definition/render_html.py
```

`visual_check.cjs`에도 같은 Playwright 모듈·브라우저 환경 변수를 적용한다.

브라우저 경로를 생략하면 Playwright의 Chromium을 쓴다. 모듈 경로를 생략하면 기존 npm 캐시 후보를 찾으며, 버전이 맞지 않으면 명시 경로를 지정한다. 패키지·브라우저를 자동 설치하지 않는다. 렌더 중 HTTP·HTTPS 요청을 차단하고 로컬 스크립트만 사용한다.

## 검사하는 것

- 9계통·본문 59개·상세 57개·하위 책임 키 62개의 구조와 대응.
- 정의 2의 생성 일치와 166개 직무 ID·이름·유형·필수 범위 필드 보존.
- 대체·접수·실행·대기 흐름의 필수 관문 22개. 관문을 하나씩 없애고 연결을 이어 붙인 22개 결함을 검출한다.
- 불명 결과의 무근거 재전송, 부분 성공·취소, 직접 자료 확보·재개·종료 경로.
- 기존 8개 제한 모형의 42개 구성과 보호 조건 누락 시 19개 반례를 임시 디렉터리에서 재실행.
- 현재 문서의 로컬 링크·제목, HTML·Mermaid의 원문 해시.

관문 검사는 선언한 그래프의 연결 검사다. 노드 안의 자연어 판단·권한 구현·실제 전문 능력을 실행하지 않는다. 표의 필드 존재도 내용의 정답을 보장하지 않는다. 반례 검토와 실제 실행 평가를 함께 수행해야 한다.

## 재현 범위와 열람

`rendered/`의 SVG는 Markdown의 Mermaid에서 생성했다. HTML은 그림을 내장하므로 오프라인 열람이 가능하며, 원본 크게 열기 링크는 프로젝트 폴더 구조를 유지할 때 사용할 수 있다. 표와 큰 흐름도는 좁은 화면에서 가로로 스크롤된다.

원문 해시는 동일 판본임을 확인한다. 브라우저·폰트·Mermaid 변경에 따라 SVG 좌표나 HTML 바이트가 달라질 수 있으므로 픽셀까지 동일하다고 주장하지 않는다. 레이아웃은 [시각 검사 기록](rendered/visual-check.json)에 검사 환경·넘침·이미지 로딩 결과를 남긴다. 화면 캡처는 `rendered/`의 PNG를 참고한다.
