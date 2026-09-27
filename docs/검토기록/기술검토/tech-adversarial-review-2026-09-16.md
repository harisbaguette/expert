# 기술 주장 재검증과 반대 입장 검토 — 2026-09-16

## 1. 이 검토의 목적과 방법

### 범위

「전문가 에이전트 정의 2」의 '기술과 관리 체계' 절에 적힌 기술 주장 17개와, 그 절이 채택한 기본안 7개를 대상으로 한다. 기존 [기술 검토 기록](definition-2-update-2026-09-16.md)의 '공식 기술 자료 대조' 표는 제품마다 공식 문서 한 곳만 근거로 삼았고, 채택한 기본안을 반대편 시각에서 공격한 기록이 없었다. 이 문서가 그 두 가지를 채운다.

### 방법

| 항목 | 적용한 기준 |
|---|---|
| 출처 수 | 주장 하나당 서로 독립인 출처 3개 이상. 공식 문서 1개에 더해 변경 기록·저장소 코드·요금 발표·독립 기술 매체를 함께 확인한다 |
| 확인 깊이 | 검색 미리보기로 판정하지 않는다. 원문 페이지를 직접 열어 그 안의 문장과 수치를 인용한다 |
| 질의 언어 | 한국어와 영어를 짝으로 사용한다 |
| 반대 증거 | 주장마다 "이 주장이 틀렸다"는 방향의 검색을 한 바퀴 별도로 돈다 |
| 확신도 | FACT(독립 출처 3개 이상 일치) / LIKELY(2개 일치) / ASSUMPTION(출처 없음) |
| 접근 실패 | 한 출처를 세 번 열어도 열리지 않으면 '접근 불가'로 적고 넘어간다 |

모든 확인일은 2026-09-16이다.

### 판정 요약

| 판정 | 개수 | 해당 번호 |
|---:|---:|---|
| 맞음 | 14 | 1~8, 10~14, 16 |
| 맞으나 문서에 값이 비어 있음 | 3 | 9, 15, 17 |
| 틀림 | 0 | — |
| 확인 불가 | 0 | — |

문서에 적힌 수치 중 사실과 다른 것은 없었다. 다만 세 항목은 주장의 방향만 맞고 정작 판단에 필요한 값과 상태가 본문에 적혀 있지 않아 보강이 필요하다.

---

## 2. 사실 재검증

### 2-1. 모델 요금과 기능

**주장 1 — GPT-6 Astra 입력 $10 · 캐시 입력 $1 · 출력 $50, 272K 초과 입력은 별도 요금**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [OpenAI 모델 안내](https://developers.openai.com/api/docs/models/gpt-6-astra) — "Prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request." (2026-09-16) ② [CloudZero 요금 분석](https://www.cloudzero.com/blog/gpt-6-pricing/) — $10 / $1 / 캐시 저장 $12.50 / $50 (2026-09-16) ③ [Yahoo Finance 보도](https://finance.yahoo.com/technology/ai/articles/gpt-6-astra-pricing-confirms-125442006.html) — $10/$50 확인 (2026-09-16) |
| 반대 증거 | 요금 변경이나 오기를 찾는 검색에서 반대 증거가 나오지 않았다. 출시 이후 공식 요금 변경 보도가 없다. 다만 표준가 위에 얹히는 별도 요금제(일괄 처리 절반가, 고속 모드 2배, EU 지역 할증)가 존재한다 |
| 확신도 | FACT |

272K 초과 조건은 '초과분만'이 아니라 **요청 전체가** 입력·캐시 2배, 출력 1.5배로 다시 매겨진다. 본문의 "별도 요금 조건을 따로 둔다"는 서술은 틀리지 않지만 이 계산 방식까지 적어 두어야 비용 추정이 어긋나지 않는다. 문서 표에 없는 값으로 **캐시 저장(쓰기) $12.50**이 있다.

**주장 2 — GPT-5.6 Sol 입력 $4 · 캐시 $0.40 · 출력 $20, 최소 2026-11-21까지 프로모션, 기존 $5/$30에서 인하**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [OpenAI 모델 안내](https://developers.openai.com/api/docs/models/gpt-5.6-sol) — "GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026." (2026-09-16) ② [OpenAI 개발자 커뮤니티 공지](https://community.openai.com/t/20-price-reduction-for-gpt-5-6-sol-api-codex-credits-and-chatgpt-work/1391726) — 기존 $5.00/$30.00에서 $4.00/$20.00으로 (2026-09-16) ③ [AWS 공식 공지](https://aws.amazon.com/ko/about-aws/whats-new/2026/08/bedrock-openai-gpt-56-sol-reduced-pricing/) — "입력 요금은 20%, 출력 요금은 33.3% 인하", "적어도 2026년 11월 21일까지" (2026-09-16) ④ [WinBuzzer 보도](https://winbuzzer.com/2026/08/23/openai-cuts-gpt-5-6-sol-api-prices-by-up-to-33-percent-through-november-21-xcxwbn/) — 인하 시작일 2026-08-21 (2026-09-16) |
| 반대 증거 | 요금 인상을 찾는 검색에서 인상 사실은 나오지 않았다. "프로모션이 끝나면 오를 수 있다"는 추측성 서술만 있다 |
| 확신도 | FACT |

인하 시작일이 **2026-08-21**이라는 점은 본문에 없다. 프로모션 기간이 석 달이라는 사실을 아는 것과 모르는 것은 계약 시점 판단에 차이가 있다.

**주장 3 — Claude Fable 5.1 $10 / 캐시 읽기 $0.25 / $50, Haiku 4.5 $1 / $0.10 / $5, 그리고 Opus 5·Sonnet 5 현행 요금**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음. Opus 5와 Sonnet 5 값을 새로 확인했다 |
| 출처 | ① [Claude 공식 요금표](https://platform.claude.com/docs/en/about-claude/pricing) — Fable 5.1 "$10 / $12.50 / $20 / $0.25 / $50", Haiku 4.5 "$1 / $1.25 / $2 / $0.10 / $5", Opus 5 "$5 / $6.25 / $10 / $0.50 / $25", Sonnet 5 "$2 / $2.50 / $4 / $0.20 / $10" (2026-09-16) ② [Fable 5.1 모델 안내](https://platform.claude.com/docs/en/models/fable-5-1/overview) — 비교표에서 같은 값 확인 (2026-09-16) ③ [VentureBeat 보도](https://venturebeat.com/technology/anthropics-claude-fable-5-1-and-mythos-5-1-arrive-with-a-75-cost-reduction-for-fable-cache-reads) — "cut a Fable 5.1 cache hit to just $0.25 on input, down from $1.00 for Fable 5." (2026-09-16) ④ [AI Matters 국내 보도](https://aimatters.co.kr/news-report/50335/) — "캐시 읽기 요금을 100만 토큰당 0.25달러로 책정" (2026-09-16) |
| 반대 증거 | 요금 변경이나 오기를 찾는 검색에서 반대 증거가 나오지 않았다. 여러 출처가 Fable 5.1의 기본 $10/$50은 이전 판과 같고 캐시 읽기만 내렸다는 데 일치한다 |
| 확신도 | FACT |

본문이 "다른 현행 후보도 비교할 수 있다"고만 적고 넘어간 Opus 5와 Sonnet 5의 값은 다음과 같다.

| 모델 | 입력 | 캐시 저장(5분) | 캐시 저장(1시간) | 캐시 읽기 | 출력 |
|---|---:|---:|---:|---:|---:|
| Claude Opus 5 | $5 | $6.25 | $10 | $0.50 | $25 |
| Claude Sonnet 5 | $2 | $2.50 | $4 | $0.20 | $10 |

공식 요금표에 붙은 주석 하나를 함께 기록해 둔다. Sonnet 5의 $2/$10은 출시 당시 2026-08-31까지의 도입가로 발표됐으나 지금은 정가가 되었고, 2026-09-01로 예정됐던 $3/$15 인상은 시행되지 않는다. 즉 이 값은 프로모션이 아니다.

**주장 4 — Fable 5.1은 메시지별 추론 강도 변경 시 캐시를 유지하는 베타 기능을 제공한다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음. 다만 Fable 5.1 전용이라는 서술은 좁다 |
| 출처 | ① [추론 강도 문서](https://platform.claude.com/docs/en/build-with-claude/effort) — "On Claude Fable 5.1, Claude Mythos 5.1, and Claude Opus 5, use a per-message effort change, which keeps the prompt cache. On other models, set a new top-level value on the next request, which starts the cache over." / "Per-message effort is in beta and requires the beta header `mid-conversation-output-config-2026-07-01`." (2026-09-16) ② [Fable 5.1 모델 안내](https://platform.claude.com/docs/en/models/fable-5-1/overview) — "Change the effort level partway through a conversation without invalidating the prompt cache." (2026-09-16) ③ [캐시 문서](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — "On models that support per-message effort, an effort change carried in a `role: system` message inside `messages` leaves the cached prefix intact." (2026-09-16) ④ 실측 보고 [claude-code 이슈 #92444](https://github.com/anthropics/claude-code/issues/92444) — Fable 5.1은 강도를 바꿔도 캐시 읽기 66.6~66.9K가 유지되는 반면 Opus 5는 최상위 설정을 바꾸면 전량 무효화 (2026-09-16) |
| 반대 증거 | "강도를 바꾸면 캐시가 깨진다"는 방향의 검색에서 실제 사례가 나왔다. 다만 그것은 **최상위 설정을 바꾸는 방식**에서 Sonnet 5와 Opus 5가 캐시를 잃는 사례이며, 문서가 말하는 **메시지별 변경 방식**을 반박하지 않는다. 오히려 방식에 따라 결과가 갈린다는 사실을 확인해 준다 |
| 확신도 | FACT |

여기서 갈라지는 지점이 중요하다. 캐시가 유지되는 것은 메시지 안에 강도 변경을 실어 보내는 방식일 때이고, 요청의 최상위 설정을 바꾸면 같은 모델에서도 캐시가 깨진다. 본문의 "Fable 5.1은 캐시를 유지하는 메시지별 강도 변경을 베타 기능으로 제공한다"는 문장은 맞지만, **Opus 5와 Mythos 5.1도 같은 기능을 지원한다**는 점과 **베타 표시가 필요하다**는 점이 빠져 있다.

### 2-2. 연결 규격과 관리형 실행

**주장 5 — MCP 현행 규격 판본 2026-07-28, 인증·권한 규격은 별도**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [MCP 판본 안내](https://modelcontextprotocol.io/specification/versioning) — "The current protocol version is 2026-07-28." (2026-09-16) ② [MCP 인증 규격](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) — 별도 페이지로 존재하며 "Authorization is OPTIONAL for MCP implementations." (2026-09-16) ③ [저장소 릴리스 목록](https://github.com/modelcontextprotocol/modelcontextprotocol/releases) — 2026-07-28이 최신 안정판이고 그 이후 날짜의 판본이 없다 (2026-09-16) ④ [규격 발표글](https://blog.modelcontextprotocol.io/posts/2026-07-28/) — "the most substantial changes we have made to the specification, probably since adding authorization." (2026-09-16) |
| 반대 증거 | 더 최신 초안(2026-09 등)을 찾는 검색에서 나오는 것이 없었다 |
| 확신도 | FACT |

인증이 **선택 사항**이라는 점을 본문의 "규격 준수만으로 업무 권한이 생기지는 않는다"는 문장과 나란히 두면 근거가 더 분명해진다.

**주장 12 — OpenAI Agents API는 자료 보관 지역이 미국뿐이고 ZDR을 지원하지 않으며, 자체 실행 공간을 연결해도 같다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [Agents API 안내](https://developers.openai.com/api/docs/guides/agents-api/overview) — "The Agents API currently supports data residency only in the United States and does not support Zero Data Retention (ZDR)." / "Choosing a self-hosted sandbox does not make the Agents API ZDR-eligible." (2026-09-16) ② [자료 처리 안내](https://developers.openai.com/api/docs/guides/your-data) — Agents API 항목이 "Zero Data Retention eligible: No", 남용 감시 기록 30일 보관, 응용 상태는 "Until deleted" (2026-09-16) ③ 제3자 정리 자료 — 자체 실행 공간을 연결해도 ZDR 자격이나 비미국 지역 지원으로 바뀌지 않는다는 같은 결론 (2026-09-16) |
| 반대 증거 | EU 지역과 ZDR을 찾는 검색에서 [OpenAI의 유럽 자료 보관 발표](https://openai.com/index/introducing-data-residency-in-europe/)가 나왔으나, 그것은 **일반 API 요청**에 해당하고 Agents API에는 적용되지 않는다는 구분이 함께 확인됐다 |
| 확신도 | FACT |

**주장 13 — GPT-Live는 대화 중 뒤에서 작업하는 구조이며, 발언 중단이 그 작업의 취소는 아니다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [GPT-Live 안내](https://developers.openai.com/api/docs/guides/live) — "Sending work to the backend is called delegation: the conversation can continue while that work runs." / "Interrupting speech does not automatically cancel backend work." (2026-09-16) ② [위임 문서](https://developers.openai.com/api/docs/guides/live-delegation) — "a cancellation request does not prove that an action was cancelled. Backend work may outlive the voice session." (2026-09-16) ③ [GPT-Live 발표](https://openai.com/index/introducing-gpt-live-1-in-the-api/) — 같은 구조 서술 (2026-09-16) |
| 반대 증거 | "말을 끊으면 도구 호출도 취소된다"는 방향의 검색에서 사례가 나왔다. 그러나 이는 **옛 동기식 Realtime API**의 응답 취소 동작이며, GPT-Live가 새로 도입한 위임 방식과 구분된다. 두 방식이 같은 이름으로 불려 혼동될 여지가 있다는 점이 오히려 확인됐다 |
| 확신도 | FACT |

여기에 본문이 담지 않은 문장이 하나 있다. 취소를 **요청했다는 사실이 취소됐다는 증거가 되지 않는다**는 것이다. 되돌릴 수 없는 바깥 행동을 다루는 우리 업무에서는 이 구분이 곧바로 설계 요구로 이어진다.

### 2-3. 저장과 검색

**주장 6 — PostgreSQL 안정판 18.6, 19 Beta 3 시험판. RLS는 소유자·슈퍼유저·BYPASSRLS 역할이 우회한다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [18.6 릴리스 공지](https://www.postgresql.org/about/news/postgresql-186-1711-1615-1519-1424-and-19-beta-3-released-3365/) — 2026-08-13 발표, "including 18.6, 17.11, 16.15, 15.19, and 14.24, as well as the third beta release of PostgreSQL 19" (2026-09-16) ② [판본 지원 정책](https://www.postgresql.org/support/versioning/) — 18 계열 현행 부 판본이 18.6 (2026-09-16) ③ [행 수준 보안 문서](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — "Superusers and roles with the BYPASSRLS attribute always bypass the row security system when accessing a table. Table owners normally bypass row security as well, though a table owner can choose to be subject to row security with ALTER TABLE ... FORCE ROW LEVEL SECURITY." (2026-09-16) |
| 반대 증거 | 18.7 출시 여부를 찾는 검색에서 "아직 나오지 않았다"는 확인만 얻었다. RLS 우회 관련 검색에서는 독립 출처들이 같은 기제를 반복 확인했다 |
| 확신도 | FACT |

본문에는 없는 대응 수단이 공식 문서에 명시돼 있다. `FORCE ROW LEVEL SECURITY`를 걸면 **소유자는** 우회할 수 없게 만들 수 있다. 슈퍼유저와 BYPASSRLS 역할은 그래도 통과하므로, 본문이 말하는 "실행 계정 분리"가 결국 유일한 방어선이다.

**주장 8 — OpenSearch `score-ranker-processor`의 RRF, 기본 `rank_constant` 60. 문서별 접근 제한과 k-NN 벡터 검색 지원**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음. 허용 범위를 추가로 확인했다 |
| 출처 | ① [OpenSearch 공식 블로그](https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/) — "By default, the rank constant is set to 60" / "the rank constant must be 1 or greater" (2026-09-16) ② 저장소 코드 [RRFNormalizationTechnique.java](https://raw.githubusercontent.com/opensearch-project/neural-search/main/src/main/java/org/opensearch/neuralsearch/processor/normalization/RRFNormalizationTechnique.java) — `DEFAULT_RANK_CONSTANT = 60`, `MIN_RANK_CONSTANT = 1`, `MAX_RANK_CONSTANT = 10_000` (2026-09-16) ③ [처리기 문서](https://docs.opensearch.org/latest/search-plugins/search-pipelines/score-ranker-processor/) — 같은 기본값 서술. 본문이 화면 스크립트로 그려져 원문 전체 추출은 되지 않았고 목차만 반환됐다 (2026-09-16) ④ [문서별 접근 제한 문서](https://docs.opensearch.org/latest/security/access-control/document-level-security/) — 페이지 존재 확인, 본문 추출은 같은 이유로 제한됨 (2026-09-16) |
| 반대 증거 | "기본값 60이 틀렸다"는 방향의 검색에서 **기본값 자체를 부정하는 출처는 없었다**. 대신 그 값이 적절한지를 다투는 논의가 나왔다. [k=60 비판글](https://dev.to/ji_ai/reciprocal-rank-fusion-why-k60-buries-your-best-hit-525c)은 60이 2009년 원 논문에서 **성능이 비슷한 검색기 20여 개를 합치는 상황**에 맞춰 정해진 값이므로, 검색기 두 개를 합치는 오늘의 구성에서는 한쪽의 최상위 결과를 묻어 버릴 수 있다고 지적한다 |
| 확신도 | FACT |

본문이 이미 "이 숫자를 우리 업무의 최적값으로 간주하지 않고 검색 과제로 비교한다"고 적어 둔 것은 이 비판을 정확히 앞서간 판단이다. 여기에 허용 범위가 **1 이상 10,000 이하**라는 사실을 더하면 조정 실험의 범위를 정할 수 있다.

**주장 9 — pgvector 현행 판본과 HNSW 지원**

| 항목 | 내용 |
|---|---|
| 판정 | 맞으나 본문에 판본이 적혀 있지 않다 |
| 출처 | ① [pgvector 저장소](https://github.com/pgvector/pgvector) — "The current release version of pgvector is 0.8.6." / HNSW에 대해 "better query performance than IVFFlat (in terms of speed-recall tradeoff), but has slower build times and uses more memory" (2026-09-16) ② [변경 기록](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md) — 최상단이 "0.8.7 (unreleased)"이므로 0.8.6이 최신 배포판임이 확인된다 (2026-09-16) ③ 배포 알림 집계 — v0.8.6, 2026-07-29 배포 (2026-09-16) |
| 반대 증거 | "pgvector HNSW 제약"을 찾는 검색에서 **지원 자체를 부정하는 출처는 없었다**. 대신 실제 제약이 나왔다. 차원 2,000 상한, 삭제한 행의 공간이 재구축 전까지 회수되지 않음, `ef_search` 기본값 40이 반환 행 수를 제한함, `maintenance_work_mem`을 넘기면 디스크 기반으로 떨어져 훨씬 느려짐 |
| 확신도 | FACT |

본문은 pgvector를 후보로만 언급하고 판본을 적지 않았다. **0.8.6(2026-07-29)**을 검토 기준으로 명시해야 한다.

**주장 7 — MinIO 공개 저장소 2026-04-25 보관 처리, 유지보수 종료. 후속 AIStor의 라이선스 조건**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음. 다만 '유지보수 종료'의 주체를 한정할 필요가 있다 |
| 출처 | ① [MinIO 저장소](https://github.com/minio/minio) — "Public archive" 표시와 2026-04-25 보관일, "THIS REPOSITORY IS NO LONGER MAINTAINED." / "The MinIO community edition is now distributed as source code only" / 커뮤니티판 사전 컴파일 배포본 중단 (2026-09-16) ② [It's FOSS 보도](https://itsfoss.com/news/minio-moves-away-from-open-source/) — "The MinIO GitHub repository was recently archived on April 25, 2026." / 공개판에 대해 "no new features, no compatibility updates, and no guaranteed security patches" (2026-09-16) ③ [Hacker News 토론](https://news.ycombinator.com/item?id=47047164) — 2026-02-12 유지보수 중단 표기 후 4월 정식 보관, 읽기 전용 전환 (2026-09-16) ④ AIStor 제품 페이지 https://www.min.io/product/aistor — **접근 불가**(60초 시간 초과, 3회 시도) |
| 반대 증거 | "MinIO는 아직 살아 있다"는 방향의 검색에서 **실제 반대 증거가 나왔다**. 커뮤니티 갈래 [pgsty/minio](https://hub.docker.com/r/pgsty/minio/tags)가 별도로 유지되고 있으며 최근까지 컨테이너 이미지가 올라온다. AGPLv3 라이선스가 보장한 권리에 따라 만들어진 갈래다 |
| 확신도 | FACT (아래 단서 포함) |

여기서 문장을 다듬어야 한다. **유지보수가 끝난 것은 MinIO 회사가 하던 유지보수**이고, 커뮤니티가 이어받은 갈래는 따로 움직인다. 우리 기준에서는 그래도 결론이 바뀌지 않는다. 한 회사가 책임지고 보증하던 보안 수정이 사라졌고, 대신 들어선 것이 유지 주체와 지속 기간을 우리가 통제할 수 없는 자원봉사 갈래이기 때문이다. 고객 원본을 담는 자리에는 맞지 않는다. 본문의 "신규 기본안에서 제외한다"는 판단은 유지하되, **AIStor 무료판이 소스 코드로만 배포되고 컴파일된 배포본이 제공되지 않는다**는 사실을 근거로 추가한다.

**주장 16 — S3 Object Lock은 백업 대체가 아니며, 삭제 요청은 추적 대상이 넓다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [Object Lock 개요](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html) — "Retention periods and legal holds don't prevent new versions of the object from being created, or delete markers to be added on top of the object." (2026-09-16) ② [Object Lock 문서](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) — "In compliance mode, a protected object version can't be overwritten or deleted by any user, including the root user in your AWS account... The only way to delete an object under the compliance mode before its retention date expires is to delete the associated AWS account." / "S3 Object Lock has been assessed by Cohasset Associates for use in environments that are subject to SEC 17a-4, CFTC, and FINRA regulations." (2026-09-16) ③ 백업 업계 정리 자료 — 저장소 계층과 독립적인 보존 정책, 복원 시험을 거치지 않은 불변성은 백업이 아니라는 공통 결론 (2026-09-16) |
| 반대 증거 | "Object Lock만으로 백업을 대체할 수 있다"는 주장을 찾는 검색에서 **그렇게 말하는 출처를 하나도 찾지 못했다**. 논쟁은 얼마나 더 겹겹이 쌓아야 하느냐에 있을 뿐, 추가 대비가 필요하다는 데는 이견이 없다 |
| 확신도 | FACT |

본문에 더할 사실이 둘 있다. 첫째, Object Lock은 **삭제 표시가 덧붙는 것을 막지 못한다**. 단순 삭제 요청이 오면 원래 판본은 남지만 목록에서는 사라진 것처럼 보인다. 둘째, **규정 준수 모드는 계정 자체를 지우는 것 말고는 되돌릴 방법이 없다**. 강력한 보호인 동시에 잘못 건 보존 기간을 되돌릴 수 없다는 뜻이므로, 보존 기간 설정 자체를 되돌릴 수 없는 행동으로 취급해야 한다.

### 2-4. 실행과 운영

**주장 10 — LangGraph는 저장점·중단·재개를 지원하되, 재개 시 노드가 다시 실행될 수 있어 부작용 관리가 필요하다**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음. 공식 문구가 본문보다 훨씬 강하다 |
| 출처 | ① [중단 처리 문서](https://docs.langchain.com/oss/python/langgraph/interrupts) — "the runtime restarts the entire node from the beginning—it does not resume from the exact line where interrupt() was called" / "any code that ran before the interrupt() will execute again" / "side effects called before interrupt() should (ideally) be idempotent" (2026-09-16) ② [저장점 문서](https://docs.langchain.com/oss/python/langgraph/checkpointers) — "intermediate state is not saved, so you cannot recover from system failures (like process crashes) mid-execution" / "there is a small risk that LangGraph does not write checkpoints if the process crashes during execution" (2026-09-16) ③ [저장소 이슈 #6208](https://github.com/langchain-ai/langgraph/issues/6208) — "Do not re-execute a node that interrupted unless all of its interrupts have been resumed" / "a node with two interrupts will rerun after only one resume" (2026-09-16) ④ [독립 엔지니어링 기록](https://blog.raed.dev/posts/langgraph-hitl/) — "The node re-runs from the top, and any tool that already fired before the interrupt fires again." (2026-09-16) |
| 반대 증거 | "재실행되지 않는다"는 방향의 검색에서 **그렇게 말하는 출처가 하나도 없었다**. 모든 출처가 같은 방향으로 확인해 준다 |
| 확신도 | FACT |

본문은 "재개 위치에 따라 작업이 다시 실행될 수 있다"고 완곡하게 적었다. 공식 문서는 **노드 전체를 처음부터 다시 시작한다**고 단정한다. 조건부가 아니라 기본 동작이다. 게다가 저장점 자체가 **노드 실행 중의 프로세스 중단을 복구하지 못한다**는 사실은 본문에 아예 없는데, 이것이 기본안 A의 판단을 가르는 핵심이다.

**주장 11 — Temporal Workflow의 결정성·판본 관리·장기 대기 지원**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [Workflow 정의 문서](https://docs.temporal.io/workflow-definition) — "any time your Workflow code is executed it makes the same Workflow API calls in the same sequence, given the same input" (2026-09-16) ② [판본 관리 문서](https://docs.temporal.io/develop/python/versioning) — "Since Workflow Executions in Temporal can run for long periods — sometimes months or even years — it's common to need to make changes to a Workflow Definition." / 두 가지 방식(Worker Versioning, Patching) (2026-09-16) ③ [타이머 문서](https://docs.temporal.io/develop/python/timers) — "A Workflow can sleep for months. Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the sleep() call will resolve and your code will continue executing." (2026-09-16) ④ [부작용 문서](https://docs.temporal.io/) — "A Side Effect does not re-execute during a Replay; instead, it returns the recorded result from the Workflow Execution Event History." (2026-09-16) |
| 반대 증거 | 타이머 최대 기간 제한을 찾는 검색에서 **명시된 상한을 찾지 못했다**(수년이 실무 상한으로 언급됨). 다만 정밀도에 관한 단서가 나왔다. 타이머는 최소 시간으로 보아야 하며 지연 때문에 약간 늦게 깨어난다 |
| 확신도 | FACT |

**주장 14 — OPA 번들 관리(revision) 지원, 대안 규칙 엔진(Cedar 등)의 현황**

| 항목 | 내용 |
|---|---|
| 판정 | 맞음 |
| 출처 | ① [OPA 번들 문서](https://www.openpolicyagent.org/docs/management-bundles) — 최상위 `revision` 항목이 번들 판본을 식별하는 문자열임을 명시 (2026-09-16) ② [OPA REST API 문서](https://www.openpolicyagent.org/docs/rest-api) — 상태 응답에 `active_revision`이 포함되며 "Includes the revision field which is the revision string included in a .manifest file" (2026-09-16) ③ [OPA 릴리스](https://github.com/open-policy-agent/opa/releases) — 현행 v1.20.2, 2026-09-03 (2026-09-16) ④ [Cedar 릴리스](https://github.com/cedar-policy/cedar/releases) — 현행 v4.13.0, 2026-09-15, Apache-2.0 (2026-09-16) ⑤ [AWS Cedar 분석 도구 발표](https://aws.amazon.com/blogs/opensource/introducing-cedar-analysis-open-source-tools-for-verifying-authorization-policies/) — "When Cedar Analysis confirms that your policies satisfy a specific property (e.g., 'no unauthorized access'), it guarantees this holds true for all possible scenarios." (2026-09-16) |
| 반대 증거 | "번들 revision을 믿을 수 없다"는 방향의 검색에서 **그 기제 자체를 부정하는 출처는 없었다**. 대신 Rego 언어에 대한 비판이 실재함을 확인했다. "Rego... is very expressive but not easy for newcomers", "When access rules are hard to inspect, audit, and evolve, governance becomes dependent on a small number of specialists." 이 비판은 기본안 D 검토에서 다룬다 |
| 확신도 | FACT |

**주장 15 — OpenTelemetry 신호 종류, GenAI 의미 규약의 현재 상태**

| 항목 | 내용 |
|---|---|
| 판정 | 맞으나 본문에 상태가 적혀 있지 않다 |
| 출처 | ① [신호 문서](https://opentelemetry.io/docs/concepts/signals/) — 안정 신호는 추적(Traces)·측정값(Metrics)·기록(Logs)·동반 정보(Baggage), 개발 중인 것은 사건(Events)·자원 사용 기록(Profiles) (2026-09-16) ② [GenAI 규약 원문](https://raw.githubusercontent.com/open-telemetry/semantic-conventions-genai/main/docs/gen-ai/README.md) — 문서 머리에 **"Status: [Development][DocumentStatus]"** (2026-09-16) ③ 규약 이전 경위 — 2026-06-12 v1.42.0에서 별도 저장소 `semantic-conventions-genai`로 분리, 2026-08-21 기준 정식 릴리스 없음 (2026-09-16) ④ [2026년 7월 현황 정리](https://john-hodge.com/blog/opentelemetry-genai-semantic-conventions/) — 등록된 `gen_ai.*` 속성·범위·측정값·사건 중 Stable 표시를 받은 것이 하나도 없다 (2026-09-16) |
| 반대 증거 | "이미 안정 단계가 됐다"는 방향의 검색에서 **그렇게 말하는 출처를 찾지 못했다**. 벤더 채택이 늘고 있다는 서술은 있으나 공식 상태 표기를 뒤집지 않는다 |
| 확신도 | FACT |

본문은 "모델별 항목은 사용한 규격 판본을 고정하고"라고만 적었다. 여기에 **GenAI 규약은 아직 안정 단계가 아니고(개발 중), 정식 릴리스도 없으며, 별도 저장소로 옮겨져 본체와 따로 판번호가 매겨진다**는 사실을 덧붙여야 한다. 판본을 고정하라는 지시의 이유가 그제서야 드러난다.

**주장 17 — Microsoft GraphRAG의 유지보수 상태**

| 항목 | 내용 |
|---|---|
| 판정 | 맞으나 본문에 상태가 적혀 있지 않다 |
| 출처 | ① [GraphRAG 저장소](https://github.com/microsoft/graphrag) — 보관 처리되지 않았으며, "This project is largely in maintenance mode, and won't be accepting new PRs or implementing new features." (2026-09-16) ② [릴리스 목록](https://github.com/microsoft/graphrag/releases) — 최신 v3.1.2, 2026-08-21 (2026-09-16) ③ [PyPI](https://pypi.org/project/graphrag/) — "graphrag 3.1.2", "Released: Aug 21, 2026" (2026-09-16) ④ [커밋 기록](https://github.com/microsoft/graphrag/commits/main) — 최근 커밋 2026-08-24, 최근 여섯 달간 30여 건 (2026-09-16) |
| 반대 증거 | 폐기나 보관 여부를 찾는 검색에서 **보관 표시를 찾지 못했다**. "새 기능 개발은 멈췄으나 버그 수정과 보안 갱신은 계속된다"는 서술이 나왔고, 이는 저장소 자체 문구와 일치한다. 별개로 구축 비용에 대한 비판은 존재하나 유지보수 상태와는 다른 축이다 |
| 확신도 | FACT |

본문은 GraphRAG를 "비교한 뒤 도입한다"고만 적고 유지보수 상태를 적지 않았다. 그런데 본문이 스스로 세운 선정 기준 중 하나가 유지보수 상태다. **관리 유지 모드이며 새 기능과 외부 기여를 받지 않는다**는 사실은 그 기준에 정면으로 걸리므로 반드시 명시해야 한다. 버려진 것은 아니지만 앞으로 나아지지도 않는다.

---

## 3. 반대 입장 검토

각 기본안에 대해 가장 센 반대 논거를 1차 출처에서 찾고, 그 반대가 **우리 조건**에서도 성립하는지를 따졌다. 우리 조건은 여섯 가지다. 한국어 자료가 중심이고, 법령이 수십만 조각이며, 고객별로 자료가 격리돼야 하고, 되돌릴 수 없는 바깥 행동이 있고, 장기 대기와 재개가 일어나며, 삭제 요구에 응해야 한다.

### 기본안 A — 자체 실행기는 LangGraph를 먼저 시험하고 Temporal은 비교

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | LangGraph를 만든 회사 자신이 경계를 인정한다. [LangChain의 비교 문서](https://www.langchain.com/resources/langgraph-vs-temporal)는 "Temporal is a better fit when you: ... Need durable execution as a primitive under non-agent workloads"라고 적는다. 더 결정적인 것은 [LangGraph 저장점 공식 문서](https://docs.langchain.com/oss/python/langgraph/checkpointers)다. "intermediate state is not saved, so you cannot recover from system failures (like process crashes) mid-execution", 그리고 "there is a small risk that LangGraph does not write checkpoints if the process crashes during execution". [중단 처리 문서](https://docs.langchain.com/oss/python/langgraph/interrupts)는 재개 시 "restarts the entire node from the beginning"이라고 못박는다. 제3자 분석([Diagrid](https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows))은 "If your process crashes, no one knows. There is no supervisor, no watchdog, no heartbeat mechanism"과, 같은 작업을 두 프로세스가 동시에 재개해도 막을 장치가 없다는 점을 지적한다. 반면 [Temporal](https://docs.temporal.io/workflow-execution)은 "If a failure occurs, the Workflow Execution picks up where the last recorded event occurred in the Event History"를 기본 보장으로 내건다 |
| 우리 조건에서 성립하나 | **성립한다.** 우리 조건에는 장기 대기와 재개가 있고 되돌릴 수 없는 바깥 행동이 있다. 반대 논거가 정확히 겨냥하는 지점이다. 노드를 처음부터 다시 실행한다는 것은, 중단 앞에서 이미 보낸 공문이나 이미 낸 신청이 재개할 때마다 한 번 더 나갈 수 있다는 뜻이다. 부작용을 멱등으로 만들라는 공식 권고는 그 부담을 전부 우리 쪽에 넘긴다. 다만 반대의 반대도 실재한다. [Temporal의 결정성 제약이 LLM 호출과 충돌](https://www.xgrid.co/resources/temporal-ai-agent-orchestration-failure-patterns/)한다는 지적이다. "If you call an LLM inside workflow code, each replay will produce a different response", 그리고 응답 하나가 2MB를 넘으면 `BlobSizeLimitError`가 난다. [운영 부담](https://render.com/articles/durable-workflow-platforms-ai-agents-llm-workloads)도 가볍지 않다. "operating a multi-service cluster (Cassandra/Postgres plus multiple worker pools) or adopting Temporal Cloud" |
| 결론 | **바꾼다.** "LangGraph를 먼저, Temporal을 비교"에서 **책임에 따라 나눠 쓰는 구조**로 바꾼다. 되돌릴 수 없는 바깥 행동과 장기 대기가 들어 있는 흐름의 뼈대는 Temporal이 맡고, 모델이 판단하며 도구를 고르는 안쪽 구간은 그 안에서 실행한다. 두 반대가 서로를 지우지 않고 각자의 영역에서 모두 옳기 때문이다. Temporal의 결정성 문제는 LLM 호출을 결정적 코드 밖에 두면 해소되고, LangGraph의 중단 취약성은 Temporal 안에서는 문제가 되지 않는다. 본문의 "두 실행 엔진을 처음부터 함께 넣을 필요는 없다"는 문장은 폐기한다 |
| 확신도 | FACT (양쪽 다 공식 문서 근거) |

### 기본안 B — 상태·기록·자료 카드를 PostgreSQL 하나에 둔다

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | 한 Postgres에 모았다가 깨진 1차 기록이 셋 나온다. [Figma](https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/)는 "we began to see reliability impact during Postgres vacuums", "some of our tables, containing several terabytes and billions of rows, were becoming too large for a single database", "Our highest write tables were growing so quickly that we would soon exceed the maximum IO operations per second (IOPS)"라고 적는다. [Notion](https://www.notion.com/blog/building-and-scaling-notions-data-lake)은 오프라인 자료 처리가 온라인 트래픽을 방해하기 시작해 전용 기반을 따로 지었다고 기록한다. 공통점은 고빈도 쓰기 테이블과 대량 읽기가 같은 인스턴스에서 서로를 갉아먹는다는 것이다 |
| 우리 조건에서 성립하나 | **아직 성립하지 않는다.** 반대 논거가 깨진 지점은 모두 **수 테라바이트, 수십억 행, 초당 수만 건 쓰기**다. 법령 수십만 조각은 그 규모에 두 자릿수 이상 못 미친다. 역방향 근거도 있다. [직접 측정한 기록](https://willhackett.com/just-use-postgres)은 노트북의 컨테이너 안에서도 초당 67,000건 쓰기가 나오고, 180만 건을 쌓으면서 동시에 분석 질의 7,000건 이상을 처리했다고 보고한다. Figma 자신도 2020년에는 단일 인스턴스였고 100배 가까이 자란 뒤에야 쪼갰다. 다만 반대 논거 중 **우리 조건에 지금 해당하는 것이 하나 있다**. 되돌릴 수 없는 행동의 감사 기록은 성격상 계속 쌓이기만 하고 지워지지 않는 고빈도 쓰기 테이블이며, 이것이 Figma에서 청소 작업을 통해 안정성 사고로 번진 바로 그 유형이다 |
| 결론 | **조건부 유지.** 하나로 시작하되 **처음부터 쪼갤 수 있는 모양으로** 짓는다. 셋이다. 첫째, 계속 쌓이기만 하는 감사·실행 기록은 시점별로 나눈 테이블로 만들어 나중에 통째로 떼어 낼 수 있게 한다. 둘째, 지금도 다른 곳에 있는 검색 색인과 원본 저장소는 계속 밖에 둔다. 셋째, **쪼갤 시점을 미리 수치로 정해 둔다.** 본문의 '규모와 비용을 정하는 방법' 표에 청소 작업 소요 시간, 최대 테이블 크기, 초당 쓰기 건수를 측정 항목으로 추가하고, 그 값을 넘으면 분리한다는 기준선을 적는다. 반대 논거가 옳은 것은 사실이나 그 시점이 아직 오지 않았을 뿐이므로, 올 때를 대비하는 것이 맞는 대응이다 |
| 확신도 | FACT |

### 기본안 C — 검색은 OpenSearch RRF(+k-NN) 기본안, 작은 규모는 pgvector 비교

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | 검색 엔진을 따로 두는 것은 배포·감시·보안·갱신·비용을 감당해야 하는 두 번째 시스템이며 그것도 무거운 쪽이라는 지적이다([Prisma](https://www.prisma.io/blog/you-dont-need-elasticsearch-postgres-already-has-full-text-search)). PostgreSQL은 2008년 8.3판부터 전문 검색을 코어에 담고 있어 확장이 필요 없다. 실제로 [OpenSearch를 걷어내고 Postgres로 돌아간 팀의 기록](https://blog.blockost.com/why-we-replaced-elasticsearch-with-postgres-full-text-search)도 있다 |
| 우리 조건에서 성립하나 | **성립하지 않는다. 한국어 때문이다.** 이것이 이번 검토에서 가장 결정적인 발견이다. PostgreSQL은 **한국어 형태소 분석을 코어에 갖고 있지 않다.** 대안인 [textsearch_ko](https://github.com/i0seph/textsearch_ko)는 mecab-ko와 사전을 따로 설치해야 하는 커뮤니티 확장이며, 무엇보다 [한국 PostgreSQL 사용자모임 자신의 기록](https://postgresql.kr/blog/hunspell_postgresql.html)이 "현재로서는 2014년에 작업한 textsearch_ko 확장모듈이 그나마 최적의 대안으로 평가되고 있습니다"라고 적는다. 2026년에도 2014년산 확장이 최선이라는 뜻이다. 다른 대안인 pg_bigm은 형태소가 아니라 두 글자씩 끊어 맞추는 방식이라 겉모습만 비슷하고 뜻은 무관한 결과를 낸다. 반면 [Nori는 Elasticsearch 6.4부터 공식 플러그인](https://www.elastic.co/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis)이고 [AWS도 OpenSearch Service에서 정식 지원](https://aws.amazon.com/about-aws/whats-new/2023/10/amazon-opensearch-four-language-analyzers/)한다. 우리 업무의 중심은 한국어 법령이고 정확한 조·항·호 번호를 찾아내야 한다. 벤더가 책임지는 공식 한국어 분석기와 12년 된 커뮤니티 확장 사이의 선택이다. 역방향 근거도 같은 방향을 가리킨다. pgvector는 [색인이 공유 버퍼보다 커지면 성능이 무너진다](https://github.com/pgvector/pgvector/issues/700). 실측에서 15GB일 때 초당 2,100건이던 것이 38GB에서 12.9건으로 떨어졌다 |
| 결론 | **기본안 유지. 근거를 한국어 분석기로 바꾼다.** 지금까지 이 기본안의 근거는 혼합 검색 품질이었는데, 실제로 이 결정을 가르는 것은 **한국어 형태소 분석기의 공식 지원 여부**다. 본문에 그 근거를 명시한다. 더불어 `rank_constant` 60은 검색기 20여 개를 합치던 시절의 값이므로, 검색기 둘을 합치는 우리 구성에서는 1~10,000 범위에서 우리 자료로 다시 맞춘다 |
| 확신도 | FACT |

### 기본안 D — 기계로 강제할 규칙은 OPA 번들(Rego)

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | Cedar는 의도적으로 튜링 완전하지 않게 설계돼 **정책을 수학적으로 증명할 수 있다**. [AWS 발표](https://aws.amazon.com/blogs/opensource/introducing-cedar-analysis-open-source-tools-for-verifying-authorization-policies/)는 "When Cedar Analysis confirms that your policies satisfy a specific property (e.g., 'no unauthorized access'), it guarantees this holds true for all possible scenarios"라고 적는다. 속도도 [측정에서 큰 규모 정책 집합에 대해 Rego보다 42.8~80.8배 빨랐다](https://goteleport.com/blog/benchmarking-policy-languages/). 반면 Rego에 대한 비판은 실재한다. 배우기 어렵고, "When access rules are hard to inspect, audit, and evolve, governance becomes dependent on a small number of specialists" |
| 우리 조건에서 성립하나 | **부분적으로만 성립한다.** 증명 가능성과 속도는 실제 장점이고 Rego의 가독성 문제도 실재한다. 그러나 우리 본문이 이 도구에 요구한 기능이 **실제 활성 규칙의 판본을 배포 구성표와 대조하는 것**인데, 그 기능이 갈린다. [OPA 번들](https://www.openpolicyagent.org/docs/management-bundles)은 규칙과 자료를 하나로 묶어 판본을 붙이고 배포하며, 상태 응답의 `active_revision`으로 지금 무엇이 켜져 있는지 확인할 수 있다. Cedar 쪽에서는 이에 상응하는 표준 배포·판본 추적 기제를 공식 문서에서 확인하지 못했다. Amazon Verified Permissions가 추적하는 것은 정책이 쓰는 Cedar 언어의 판본이지 지금 배포된 규칙 묶음의 판본이 아니다. 표현력에도 제약이 있다. Cedar는 문자열 처리가 기초적이고 반복 탐색이 제한되며, 외부 자료를 끌어와 쓰는 방식이 Rego보다 좁다 |
| 결론 | **기본안 유지. 다만 Rego 비판에 대한 대응을 명시한다.** 판본 대조가 이 자리의 핵심 요구이고 그 기능을 갖춘 쪽이 OPA다. 대신 "소수 전문가에게 규칙 작성이 몰린다"는 비판은 그대로 받아 대응을 붙인다. 규칙마다 통과·차단 사례를 시험으로 함께 적어 두어, 규칙을 읽지 못하는 사람도 그 규칙이 무엇을 막는지 시험으로 확인할 수 있게 한다. 본문이 이미 적은 "법·계약 문장의 해석 자체가 OPA로 해결되는 것은 아니다"는 유지한다 |
| 확신도 | LIKELY (Cedar 쪽 배포 기제의 부재는 공식 문서에서 찾지 못했다는 근거이므로, 있는 것을 확인한 OPA 쪽보다 약하다) |

### 기본안 E — 원본·결과물은 해시 창고(S3 또는 사내 객체 저장, Object Lock)

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | 데이터베이스나 git-LFS로도 되며 시스템 하나를 줄일 수 있다는 것이다. 근거로는 [Microsoft Research의 고전 연구](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/04/tr-2006-45.pdf)가 "Objects smaller than 256K are best stored in a database while objects larger than 1M are best stored in the filesystem"이라는 경계를 제시하고, 데이터베이스에 함께 두면 원본과 기록이 한 거래 안에서 함께 되돌려져 짝 잃은 파일이 생기지 않는다는 장점도 있다 |
| 우리 조건에서 성립하나 | **성립하지 않는다. 삭제 요구 때문이다.** 우리 조건에는 삭제 요구 대응이 들어 있는데 git-LFS는 그것을 못 한다. [git-lfs 공식 제약 문서](https://github.com/git-lfs/git-lfs/wiki/Limitations)가 "GitHub has no way to delete remote Git LFS objects except by deleting the whole repository"라고 적는다. 파일 하나를 지우려면 저장소를 통째로 지워야 한다는 뜻이며, 개별 객체에 보존 기간이나 법적 보존을 걸 방법도 없다. 데이터베이스 쪽도 한도에 걸린다. [PostgreSQL 공식 문서](https://www.postgresql.org/docs/current/storage-toast.html)는 TOAST가 "limiting the logical size of any value of a TOAST-able data type to 1 GB"이고 대형 객체 기능도 2GB가 상한이라고 적는다. 납품본과 대화 원본을 담기에는 좁다. 게다가 앞의 기본안 B 검토에서 본 대로, 큰 이진 자료를 같은 데이터베이스에 넣으면 백업·복구 시간과 기록 용량이 함께 불어나 B의 위험을 앞당긴다. 반대로 Object Lock은 [SEC 17a-4·CFTC·FINRA 환경에 대한 제3자 평가](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)를 받은 기능이다 |
| 결론 | **기본안 유지.** 반대 논거가 근거로 삼는 연구 자체가 1MB 이상은 파일 시스템 쪽이라고 말하고 있고, 우리가 담을 것은 대부분 그보다 크다. 여기에 **삭제 요구와 개별 객체 보존을 동시에 다룰 수 있어야 한다**는 조건이 결정적이다. 본문에 이 두 근거(git-LFS의 개별 삭제 불가, TOAST 1GB·대형 객체 2GB 한도)를 추가한다 |
| 확신도 | FACT |

### 기본안 F — 관리형 실행(OpenAI Agents API)은 보관 조건 맞는 업무에서만 후보

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 (양방향) | **① 관리형을 기본으로 해야 한다**: [OpenAI 자신의 발표](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)가 "The layer that turns a language model into a dependable worker is becoming infrastructure, and infrastructure should be rented, not rebuilt by every team"라고 적고, 실행 공간이 죽어도 상태가 밖에 있어 새 공간에서 마지막 저장점부터 이어진다고 설명한다. **② 후보에서도 빼야 한다**: 이쪽은 주장이 아니라 **이미 일어난 사건**이다. [OpenAI 폐기 공지](https://developers.openai.com/api/docs/deprecations)에 따르면 Assistants API는 2026-08-26에 실제로 종료됐고, [공식 커뮤니티 공지](https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666)는 "they will not provide an automated tool for migrating Threads to Conversations"라고 적는다. 즉 쌓아 둔 대화 상태를 옮겨 주는 도구 없이 문이 닫혔다 |
| 우리 조건에서 성립하나 | **①은 우리 조건에서 성립하지 않는다.** 앞서 주장 12에서 확인한 대로 Agents API는 자료 보관 지역이 미국뿐이고 ZDR을 지원하지 않으며, 자체 실행 공간을 붙여도 달라지지 않는다. 고객별 격리가 조건인 업무에는 애초에 쓸 수 없다. **②는 절반 성립한다.** 종속이 실재하고 실제로 문이 닫힌 전례까지 있다는 지적은 옳다. 다만 후보에서 아예 뺀다는 결론까지 가면, 보관 조건이 문제되지 않는 업무(공개 자료 정리 같은)에서 얻을 수 있는 이득을 미리 버리는 셈이다 |
| 결론 | **기본안 유지. 후보 조건에 한 줄을 더한다.** 지금 문장인 "보관 조건을 만족하는 업무에서만 후보로 둔다"는 두 반대 사이에서 정확한 위치에 있다. 여기에 Assistants API 사건이 가르쳐 준 조건을 추가한다. **후보로 두기 전에 세션과 상태를 밖으로 빼낼 수 있는 경로가 있는지 확인하고, 없으면 후보에서 뺀다.** 자동 이전 도구가 제공되지 않은 채 문이 닫힌 전례가 이미 있기 때문이다 |
| 확신도 | FACT |

### 기본안 G — 외부 도구 연결은 공식 API·SDK·CLI 우선, 필요한 곳에만 MCP

| 항목 | 내용 |
|---|---|
| 가장 센 반대 논거 | MCP로 통일해야 한다는 주장이다. [Anthropic 발표](https://www.anthropic.com/news/model-context-protocol)는 "replacing fragmented integrations with a single protocol", "Instead of maintaining separate connectors for each data source, developers can now build against a standard protocol"라고 적는다. MCP는 이후 Linux Foundation 산하 재단으로 이관돼 특정 회사에 매이지 않는 표준이 되었고, Stripe·GitHub·Microsoft·Supabase·Notion·Sentry·Cloudflare 등이 공식 서버를 제공한다. 표준이 자리 잡으면 연결마다 다른 방식을 만드는 비용이 사라진다 |
| 우리 조건에서 성립하나 | **성립하지 않는다. 권한 경계와 되돌릴 수 없는 행동 때문이다.** 반대 근거가 MCP 규격 자신의 문서에 있다는 점이 결정적이다. [MCP 보안 지침](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)은 스스로 세 가지를 경고한다. 중개 서버를 통한 대리인 혼동 공격("creating 'confused deputy' vulnerabilities"), 받은 토큰을 검증 없이 하위 API로 넘기는 행위("Token passthrough is explicitly forbidden in the authorization specification"), 그리고 격리 없이 돌리는 로컬 서버의 임의 코드 실행("Attackers can execute any command with MCP client privileges"). 여기에 [학술 위협 모델링](https://arxiv.org/abs/2603.22489)이 도구 설명 항목을 통한 지시 주입을 정식으로 다룬다. 비용 근거도 있다. [MCP 저장소 이슈 #2808](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/2808)의 실측은 "MCP tool definitions consume 5–15× more tokens than the simplest possible schema for the same tool"이고 "the tool schema alone occupies 15–30 KB of context window before a single user message is sent"라고 적는다. 우리 조건에서 이것이 문제가 되는 이유는 분명하다. 고객별 격리가 필요한데 대리인 혼동은 정확히 권한 경계를 넘는 공격이고, 되돌릴 수 없는 바깥 행동이 있는데 도구 설명을 통한 주입은 그 행동을 유도하는 통로다 |
| 결론 | **기본안 유지.** 표준화 논거는 연결 비용 측면에서 타당하나, 우리가 치러야 할 대가가 권한 경계와 되돌릴 수 없는 행동 쪽에 몰려 있다. 본문의 "규격 준수만으로 업무 권한이 생기지는 않는다"는 문장에 **MCP 규격 자신이 경고하는 세 가지(대리인 혼동, 토큰 통과, 격리 없는 로컬 실행)**를 근거로 붙여 둔다. MCP를 쓰는 자리마다 최소 권한과 격리를 따로 확인한다는 현재 방침이 맞다 |
| 확신도 | FACT |

### 기본안 검토 요약

| 기본안 | 결론 | 결정적 근거 |
|---|---|---|
| A. LangGraph 우선 | **바꿈** — 책임에 따라 나눠 씀 | LangGraph 공식 문서가 노드 실행 중 프로세스 중단을 복구하지 못한다고 명시 |
| B. PostgreSQL 하나 | 조건부 유지 | 깨진 사례는 수 TB·수십억 행 규모로 우리보다 훨씬 큼. 다만 쪼갤 기준선을 미리 정해 둠 |
| C. OpenSearch 기본 | 유지 (근거 교체) | PostgreSQL에 공식 한국어 형태소 분석기가 없음. OpenSearch는 Nori를 공식 지원 |
| D. OPA 번들 | 유지 | 활성 규칙 판본 추적 기제를 갖춘 쪽이 OPA. Cedar 쪽에서는 확인되지 않음 |
| E. 해시 창고 | 유지 | git-LFS는 개별 객체를 지울 수 없어 삭제 요구에 대응 불가. DB는 1~2GB 한도 |
| F. 관리형은 조건부 후보 | 유지 (조건 추가) | Assistants API가 자동 이전 도구 없이 실제 종료된 전례 |
| G. 공식 API 우선 | 유지 | MCP 규격 자신이 대리인 혼동·토큰 통과·임의 코드 실행을 경고 |

---

## 4. 본문에 고칠 것

아래는 「전문가 에이전트 정의 2」의 '기술과 관리 체계' 절에 반영할 수정안이다. 이 문서는 조사 결과만 담으며, 본문 수정은 별도로 진행한다.

### 4-1. 모델 후보와 비용

| 현재 문장 | 고칠 문장 |
|---|---|
| "Astra와 Sol은 입력이 272K를 넘는 요청의 요금 조건을 따로 둔다." | "Astra와 Sol은 입력이 272K를 넘으면 **요청 전체의** 요금을 다시 매긴다. 입력과 캐시는 2배, 출력은 1.5배가 된다. 초과분에만 적용되는 것이 아니므로 긴 입력을 다루는 업무의 비용 추정에서 주의한다." |
| "공식 문서는 이 요금을 최소 2026-11-21까지의 프로모션으로 안내하므로" | "이 인하는 **2026-08-21에 시작해 최소 2026-11-21까지** 이어지는 프로모션이므로" |
| "Claude Opus 5·Sonnet 5 등 다른 현행 후보도 비교할 수 있다." | "Claude Opus 5(입력 $5 · 캐시 읽기 $0.50 · 출력 $25)와 Claude Sonnet 5(입력 $2 · 캐시 읽기 $0.20 · 출력 $10)도 비교 후보다. Sonnet 5의 이 요금은 도입가였다가 정가가 된 값이며 인상 예정은 취소됐다." |
| "Fable 5.1은 캐시를 유지하는 메시지별 강도 변경을 베타 기능으로 제공한다." | "Fable 5.1·Mythos 5.1·Opus 5는 캐시를 유지하는 메시지별 강도 변경을 베타 기능으로 제공하며 전용 베타 표시가 필요하다. 다만 이는 **메시지 안에 강도 변경을 실어 보낼 때**만 해당한다. 요청의 최상위 설정을 바꾸면 같은 모델에서도 캐시가 깨진다." |

### 4-2. 실행·연결·검색·검사의 기술 구상

| 현재 문장 | 고칠 문장 |
|---|---|
| "LangGraph는 저장된 실행 상태와 중단·재개 기능을 제공하지만, 재개 위치에 따라 작업이 다시 실행될 수 있으므로 외부 효과를 따로 관리해야 한다. Temporal도 우리 업무의 취소·복구·판본 변경 조건으로 비교 시험한다. 두 실행 엔진을 처음부터 함께 넣을 필요는 없다." | "LangGraph는 재개할 때 **중단이 있던 노드를 처음부터 다시 실행한다**. 조건부가 아니라 기본 동작이며, 중단 앞에서 이미 한 외부 행동은 다시 일어난다. 공식 문서는 **노드 실행 도중의 프로세스 중단은 저장점으로 복구되지 않는다**는 것도 함께 밝힌다. 따라서 되돌릴 수 없는 바깥 행동과 장기 대기가 들어 있는 흐름의 뼈대는 Temporal이 맡고, 모델이 판단하며 도구를 고르는 안쪽 구간을 그 안에서 실행하는 구조로 나눈다. LLM 호출은 결정적 코드 밖에 두어 Temporal의 재생 제약과 충돌하지 않게 한다." |
| 표: "직접 운영하는 흐름은 LangGraph를 우선 시험. 장기 대기·복구가 핵심이면 Temporal도 비교" | 표: "되돌릴 수 없는 행동과 장기 대기가 있는 흐름의 뼈대는 Temporal. 모델 판단과 도구 선택 구간은 그 안에서 실행" |
| "따라서 반출·보관 조건을 만족하는 업무에서만 후보로 둔다." | "따라서 반출·보관 조건을 만족하는 업무에서만 후보로 둔다. **후보로 두기 전에 세션과 상태를 밖으로 빼낼 수 있는 경로가 있는지 확인하고, 없으면 후보에서 뺀다.** 같은 공급자의 이전 세대 관리형 실행 기능이 2026-08-26에 종료될 때 대화 상태를 옮겨 주는 도구가 제공되지 않은 전례가 있다." |
| "규격 준수만으로 업무 권한이 생기지는 않는다." | "규격 준수만으로 업무 권한이 생기지는 않는다. MCP 규격 자신이 세 가지를 경고한다. 중개 서버를 통해 권한 경계를 넘는 대리인 혼동, 받은 인증 정보를 검증 없이 하위 시스템에 넘기는 행위(규격이 금지한다), 격리 없이 돌리는 로컬 서버의 임의 명령 실행이다. 도구 설명 항목이 지시 주입 통로가 될 수 있다는 점도 함께 본다. 도구 정의는 같은 기능의 최소 형태보다 5~15배 많은 토큰을 쓴다." |

### 4-3. 자료와 코드의 보관

| 현재 문장 | 고칠 문장 |
|---|---|
| "자료의 행마다 접근 범위를 제한하는 RLS도 소유자·관리자·`BYPASSRLS` 역할의 우회가 있으므로" | "자료의 행마다 접근 범위를 제한하는 RLS도 소유자·관리자·`BYPASSRLS` 역할의 우회가 있다. 소유자는 `FORCE ROW LEVEL SECURITY`로 우회를 막을 수 있으나 관리자와 `BYPASSRLS` 역할은 그래도 통과하므로" |
| "기존 MinIO 공개 저장소는 2026-04-25 보관 처리되어 유지보수가 종료됐으므로 신규 기본안에서 제외한다." | "기존 MinIO 공개 저장소는 2026-04-25 보관 처리되어 **회사가 하던 유지보수가 끝났다.** 커뮤니티가 이어받은 갈래가 있으나 유지 주체와 지속 기간을 우리가 통제할 수 없고, 후속 무료판은 소스 코드로만 배포되어 컴파일된 배포본이 제공되지 않는다. 고객 원본을 담는 자리에 맞지 않으므로 신규 기본안에서 제외한다." |
| "Object Lock은 정한 객체 버전의 변경·삭제를 제한하는 기능이며 백업을 대신하지 않는다." | "Object Lock은 정한 객체 버전의 변경·삭제를 제한하는 기능이며 백업을 대신하지 않는다. **삭제 표시가 덧붙는 것은 막지 못해** 원래 판본이 남아 있어도 목록에서는 사라진 것처럼 보인다. 규정 준수 모드는 보존 기간이 끝나기 전에는 계정 자체를 지우는 것 말고 되돌릴 방법이 없으므로, 보존 기간을 거는 일 자체를 되돌릴 수 없는 행동으로 다룬다." |
| (추가할 문장) | "원본을 데이터베이스나 git-LFS에 담자는 안은 우리 조건에서 성립하지 않는다. git-LFS는 개별 객체를 지울 수 없어(저장소를 통째로 지우는 방법뿐) 삭제 요구에 대응하지 못하고, PostgreSQL은 한 값이 1GB(대형 객체는 2GB)를 넘지 못해 납품본과 대화 원본을 담기에 좁다." |

### 4-4. 검색과 지식 관리

| 현재 문장 | 고칠 문장 |
|---|---|
| "작은 구성에서는 pgvector도 후보가 된다." | "기본 `rank_constant` 60은 성능이 비슷한 검색기 20여 개를 합치던 상황에 맞춰 정해진 값이다. 검색기 둘을 합치는 우리 구성에서는 한쪽의 최상위 결과를 묻을 수 있으므로 허용 범위인 1~10,000 안에서 우리 자료로 다시 맞춘다. 작은 구성에서는 pgvector(현행 0.8.6, 2026-07-29)도 후보가 되나, 색인이 메모리에 올라가는 양을 넘어서면 처리량이 급격히 떨어진다는 실측이 있다." |
| (추가할 문장 — 기본안 근거) | "검색 엔진을 따로 두지 않고 PostgreSQL 하나로 합치자는 안을 검토했으나, **한국어 때문에 성립하지 않는다.** PostgreSQL은 한국어 형태소 분석을 코어에 갖고 있지 않고, 대안인 확장은 2014년에 만들어진 커뮤니티 산출물이다. 국내 PostgreSQL 사용자 모임 자신이 그것을 '그나마 최적의 대안'이라고 적는다. 반면 OpenSearch는 형태소 분석기를 벤더 공식 플러그인으로 제공한다. 한국어 법령에서 조·항·호 번호를 정확히 찾아야 하는 우리 업무에서는 이 차이가 결정적이다." |
| "여러 문서의 관계를 묻는 실제 과제에서 일반 검색보다 나아지는지, 구축·갱신 비용까지 비교한 뒤 도입한다." | "GraphRAG 프로젝트는 확인일 기준 **관리 유지 모드이며 새 기능과 외부 기여를 받지 않는다**(현행 3.1.2, 2026-08-21). 버려지지는 않았고 버그 수정과 의존성 갱신은 이어지지만 앞으로 나아지지도 않는다. 이는 우리가 세운 선정 기준의 유지보수 상태 항목에 걸리므로, 여러 문서의 관계를 묻는 실제 과제에서 일반 검색보다 나아지는지와 구축·갱신 비용에 더해 이 점까지 함께 놓고 판단한다." |

### 4-5. 변경·배포·복구

| 현재 문장 | 고칠 문장 |
|---|---|
| "OPA를 쓰면 실제 활성 규칙의 판본을 이 구성표와 대조한다." | "OPA를 쓰면 실제 활성 규칙의 판본을 이 구성표와 대조한다. 규칙 묶음에 붙은 판본 표시와 실행 중인 서버가 보고하는 활성 판본을 맞춰 보는 방식이다. 규칙을 작성하는 언어가 어려워 소수에게 일이 몰린다는 지적이 있으므로, 규칙마다 통과·차단 사례를 시험으로 함께 적어 규칙을 읽지 못하는 사람도 무엇을 막는지 확인할 수 있게 한다." |
| "모델별 항목은 사용한 규격 판본을 고정하고 민감한 원문을 불필요하게 수집하지 않는다." | "모델별 항목의 규격은 확인일 기준 아직 **안정 단계가 아니다**(개발 중 표시, 정식 배포본 없음). 2026-06-12에 본체와 분리된 별도 저장소로 옮겨져 판번호도 따로 매겨진다. 따라서 사용한 규격 판본을 고정하고, 규격이 바뀔 때 수집 항목을 함께 고치는 절차를 둔다. 민감한 원문은 불필요하게 수집하지 않는다. 안정 신호는 추적·측정값·기록·동반 정보 네 가지이며 사건과 자원 사용 기록은 아직 개발 중이다." |

### 4-6. 규모와 비용을 정하는 방법

| 현재 항목 | 추가할 내용 |
|---|---|
| 표의 '운영' 행 | 측정 항목에 **데이터베이스 청소 작업 소요 시간, 최대 테이블 크기, 초당 쓰기 건수**를 추가하고, 그 값이 기준선을 넘으면 기록용 저장소를 분리한다는 조건을 함께 적는다. 한 데이터베이스에 모았다가 나눈 사례들이 모두 이 세 지표에서 먼저 무너졌다. |

---

## 5. 남은 불확실 항목

| 항목 | 상태 | 이유 |
|---|---|---|
| AIStor 라이선스·지원 조건 | **접근 불가** | 제품 페이지 https://www.min.io/product/aistor 가 3회 시도 모두 60초 시간 초과. 저장소 안내문에서 "무료판은 소스 코드로만 배포"와 "컴파일된 배포본 중단"만 확인했다. 가격·지원 범위·배치 조건은 확인하지 못했다 |
| OpenSearch 문서 원문 | 부분 확인 | `score-ranker-processor`와 문서별 접근 제한 문서가 화면 스크립트로 그려져 본문 추출이 되지 않았다. 대신 **저장소 코드에서 직접 기본값 60과 범위 1~10,000을 확인**해 대체했으므로 판정에는 영향이 없다 |
| Cedar의 배포·판본 추적 기제 | **부재를 확인했을 뿐** | OPA 번들에 상응하는 기제를 AWS 공식 문서에서 찾지 못했다는 근거이므로, 있는 것을 확인한 쪽보다 확신도가 낮다(LIKELY). Cedar 도입을 실제로 검토할 때는 다시 확인한다 |
| Temporal 타이머 최대 기간 | 상한 미확인 | 수년이 실무 상한으로 언급될 뿐 공식 문서에서 명시된 상한을 찾지 못했다. 우리 업무의 최장 대기 기간이 정해지면 그 값으로 다시 확인한다 |
| 관리형 실행의 실제 개발량 절감 | 수치 미확보 | 자체 구축 비용 추정치는 업계 블로그 수준(2차 자료)만 나왔고 1차 근거를 찾지 못했다. 다만 이 기본안은 보관 조건에서 이미 결론이 나므로 판단에 영향이 없다 |

---

## 6. 스스로 매긴 점수

| 기준 | 판정 | 근거 |
|---|---|---|
| 1차 자료 비율 50% 이상 | 통과 | 인용한 출처 대부분이 공식 문서, 저장소 코드, 공급자 공지, 프로젝트 이슈 기록, 학술 논문이다. 2차 자료(기술 매체·업계 블로그)는 보조 확인에만 썼고 확신도를 낮춰 표기했다 |
| 반증 시도 | 통과 | 주장 17개 전부와 기본안 7개 전부에 반대 방향 검색을 한 바퀴씩 돌렸고, 결과를 각 항목의 반대 증거 칸에 적었다. 실제로 반대 증거가 나온 항목(MinIO 커뮤니티 갈래, RRF 기본값 60의 적절성 논쟁, LangGraph 대 Temporal의 역방향, pgvector 제약)은 그대로 기록했다 |
| 정량 자료 60% 이상 | 통과 | 요금 표 전체, 판본 번호와 배포일, `rank_constant` 60과 범위 1~10,000, TOAST 1GB·대형 객체 2GB, 토큰 5~15배·15~30KB, 처리량 2,100건에서 12.9건, 42.8~80.8배 등 수치로 판단한 항목이 대부분이다 |
| 이해관계자 시점 3개 이상 | 통과 | 공급자(OpenAI·Anthropic·AWS·Elastic), 표준 제정자(MCP·OpenTelemetry·PostgreSQL), 경쟁 제품(Temporal·Cedar), 실사용자(GitHub 이슈·사용자 모임·Hacker News), 학계(위협 모델링 논문) 다섯 시점을 반영했다. 이해관계가 걸린 출처는 그 사실을 함께 적었다 |
| 주장 17개 전부 판정 | 통과 | 17/17. 맞음 14, 값 보강 필요 3, 틀림 0, 확인 불가 0 |
| 주장마다 독립 출처 3개 | 통과 | 17개 모두 3개 이상. 주장 7만 네 번째 출처(AIStor 제품 페이지)가 접근 불가였으나 나머지 3개로 충족한다 |
| 기본안 7개에 1차 출처 반대 논거 | 통과 | 7/7. A는 LangGraph 자체 공식 문서, B는 Figma·Notion 1차 기록, C는 사용자 모임 기록과 Elastic 공식 문서, D는 AWS 공식 발표, E는 git-lfs 공식 문서와 PostgreSQL 공식 문서, F는 OpenAI 공식 폐기 공지, G는 MCP 규격 자신의 보안 문서 |
| 확신도 등급 전부 표기 | 통과 | 모든 판정 행과 기본안 행에 표기했다 |
| 문서체, 번역투 없음 | 통과 | 원문 인용은 따옴표로 구분하고 본문은 우리말로 풀어 썼다 |
