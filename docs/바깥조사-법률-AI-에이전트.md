# 바깥 조사 — 법률 전문 AI 에이전트 (전 세계)

진행 계획 3단계 "바깥 조사 — 남이 만든 에이전트 비교" 의 첫 직종임. 확인일 2026-09-11. 검색 일꾼 5명 + 하위 7명이 모은 1차 자료를 부모가 대조해 씀. 확신도는 FACT(1차 자료 직접 확인) · LIKELY(2차 자료 또는 자체 발표만) · 미확인 으로 붙임.

## 한 줄 결론

전 세계 어디에도 **사람 없이 사건 하나를 끝까지 맡는 법률 AI 는 없음**. 30여 개 제품 전부 "변호사가 검토·승인·서명" 하는 구조이고, 우리 문서의 "대체의 뜻" 기준으로는 아직 아무도 대체가 아님. 대신 **한 단계짜리 일(문서 질문·조사·초안)은 이미 변호사 평균을 넘었고, 여러 단계를 스스로 이어 끝내는 일은 최고 모델도 10건 중 1건을 못 채움** — 이 틈이 우리가 채울 자리임.

## 1. 지도 — 다섯 갈래

| 갈래 | 누가 쓰나 | 대표 제품 (나라) | 규모 (최신 발표) | 사람이 끼는 자리 |
|---|---|---|---|---|
| 로펌 종합 플랫폼 | 대형 로펌·사내법무 | Harvey (미), Legora (스웨덴), CoCounsel (Thomson Reuters), Lexis+ Protégé (LexisNexis) | Harvey 기업가치 $15.6B · 연매출 $400M+ (2026-09) / Legora $5.6B · $150M (2026-Q2) | "결과물은 검토 준비 상태(review-ready)" — 변호사가 최종 판단 |
| 계약·사내법무 | 회사 법무팀·영업·구매 | Luminance (영), Ironclad (미), Spellbook (캐), Juro·Genie (영), LegalOn (일), MNTSQ (일), Eudia (미) | LegalOn 연매출 100억엔 · 고객 7,000+ (2025-10) / Spellbook 고객 4,000 (2025-10) | 위험도별 게이트 — 표준 계약은 이탈 때만, 큰 계약은 변호사 전권 |
| 소송 특화 (원고측 인신사고) | 미국 원고측 로펌 | EvenUp (미, $2B), Eve (미, $1B), Supio (미) | EvenUp 로펌 2,000+ · 누적 배상금 $10B+ / Eve 로펌 800~1,200 | 청구서를 로펌에 넘김. 보험사에 직접 안 보냄. 사람 100명+ 이 매주 검수 |
| AI 로펌 | 의뢰인 직접 | Crosby (미, 변호사 50+ 보유), Garfield (영, SRA 인가 첫 AI 로펌) | Crosby 계약 총액 $1B 돌파 (2026-03) / Garfield 편지 1통 £2, 소액 채권 £10k 이하 | Crosby "모든 산출물을 변호사가 검토". Garfield 는 규제기관 인가 안에서 절차 문서만 |
| 소비자 직접 | 일반인 | DoNotPay (미) | FTC 제재 $193,000 (2025-02 확정) — "로봇 변호사" 허위 주장 | 변호사 없음 → 제재됨. 이 갈래는 규제로 막힘 |

한국·일본·중국·유럽 따로 정리는 4절.

## 2. 제품별 — 실제로 무엇을 스스로 하나

| 제품 | 스스로 하는 것 (기능명 · 출시) | 못 하는 것 · 사람 자리 | 성능 주장 (근거) | 확신도 |
|---|---|---|---|---|
| Harvey | Workflow Agents · Agent Builder (2025 중반). 고객이 만든 맞춤 에이전트 25,000+개. 600+ 법률 DB 연결. 커넥터 라이브러리(2026-06, MCP 로 iManage·NetDocuments 등) | 서명·제출 없음. "Delegate the work. Own the judgment" | 환각률 0.2% (자체 BigLaw Bench) | FACT(기능) / LIKELY(수치) |
| Legora | Workflows(분류·조건문·역할 권한) · Legora Agent (2026 "에이전트의 해") · Tabular 대량 검토 | "핵심 지점에서 사람 개입" — 임계값 비공개 | Claude 채택 뒤 평가셋 18% 향상 (자체) | LIKELY |
| CoCounsel Legal | Deep Research + 안내형 워크플로 (2025-08). 사람 없이 1만 건 문서 검토 베타 (2025-11). 2026-08 차세대 = Claude Agent SDK 위에 재설계, 조사→인용 달린 결과물까지 한 흐름 | Brief Builder 가 사람 개입 지점에서 멈춤 | 구제품(Westlaw AI-AR) 환각 33% (Stanford 2024) — 신제품 수치 없음 | FACT(기능) |
| Lexis+ Protégé | 2025-01 정식. 2026-02 Lexis+ AI 완전 대체. 에이전트 4개(조정·조사·웹·고객문서) · 미리 만든 워크플로 300+ | Shepard's "At Risk" 경고로 인용 오류 3종 탐지 | 구제품 환각 17% (Stanford 2024) | FACT(기능) |
| Luminance | **Autonomous Negotiation** — 상대편 AI 와 문구를 직접 주고받아 협상 (2023-11 첫 시연, 2026 봄 전체 출시). "Autonomous by default, human in the loop by choice" | 서명만 사람. 제3자 평가: 표준 조항 87%, 비정형 72%, 위양성 14% | 검토 시간 90% 절감 (자체) | FACT(기능) / LIKELY(수치) |
| Ironclad | 에이전트 8종 (2025-11) · Act Mode = 한 문장으로 여러 에이전트 조율 (2026-04) | **위험도 3단계 게이트** — 저: 표준 NDA 이탈 때만 검토 / 중: 발송 전 변호사 검토 / 고·신규: 변호사 전권. 모든 행동 불변 감사기록 | 접수 시간 50% 단축 (자체) | FACT(기능) / LIKELY(게이트 세부) |
| Spellbook | Associate — 여러 문서에 걸친 초안·수정 (Word 안, 추적변경으로 제시) | 변호사가 수락·거부·편집해야 반영. "협상 전략·승인·법적 판단·최종 수정은 변호사 책임" 명시 | 수치 없음 | FACT |
| EvenUp | Piai 모델 (해결 사건 20만 건 학습). Express(AI 만, 몇 분) / Expert(AI+직원, 1~5일) 청구서 | 직원 100명+ 이 매주 수천 건 재작성. 2024-12 보도: "AI 라 했지만 사람이 새벽 3시까지 수작업" | 의료비 항목 정확도 95% vs GPT-4 80% (자체) · 한도액 합의 69% 더 많음 (자체) | FACT(구조) / LIKELY(수치) |
| Eve | Eve 2.0 (2026-01) Agents·Auditor·Analyst. 음성 접수 에이전트 Jenny (2025-10, 24시간 전화 응대) | "아무것도 혼자 돌지 않음. 모든 행동은 사람 체크포인트를 거침". 음성 에이전트는 법률 자문 금지 장치 | 소장 초안 5시간→1시간 (자체) | FACT |
| Crosby | 조사·분석·초안 에이전트 + 협상 음성 에이전트 + 상대편 반응 시뮬레이션 | "AI 도구가 아니라 로펌". 변호사 50+ 가 모든 일을 검토. 로펌 법인 + 기술 법인 이원 구조 (추정) | 요청 90% 를 몇 시간 안에 (자체). "로펌이 6주 걸린 일을 12시간에" (고객 인용) | FACT(구조) / LIKELY(수치) |
| Garfield | 청구서 올리면 독촉 편지(£2)·소송 예고 편지(£7.50)·소액 법원 절차까지 | SRA 인가 조건 안에서. 2025-05 첫 승소 £7,000 — 서류는 AI, 법정은 사람 변호사 | 건수 미공개 | FACT(가격) / LIKELY(인가 세부) |
| Robin AI | Reports — 수천 건 일괄 분석. Agent mode (플레이북 안 표준 NDA 자동 수정, 복잡 조항은 에스컬레이션) | 2025-11 자금난 · 영국 국세청 청산 청원 · 인력 1/3 감원. 2026-01 Microsoft 가 팀 채용 | 93% 빨라짐 (자체) | FACT(경영 상황) |
| Supio | Supio Agent — 의료 기록 연표·청구서·소송 초안·다건 분석 | "전문가 검증 결합" 만 명시 | "환각 없음" 주장에 근거 없다고 TechCrunch 가 지적 | LIKELY |

## 3. 진짜 실력 — 제3자 증거

| 무엇을 재나 | 결과 | 뜻 | 출처 · 날짜 | 확신도 |
|---|---|---|---|---|
| Vals VLAIR 1차 (문서 질문·요약·계약 수정 등 7과제) | Harvey 문서 Q&A 94.8% 최고. **계약 수정(redlining)·EDGAR 조사는 변호사(79.7%·70.1%)가 모든 AI 를 이김** | 읽고 답하기는 넘었고, 고쳐 쓰기는 아직 사람 | vals.ai 2025-02-27 | FACT |
| Vals VLAIR 조사 과제 | 변호사 71% vs AI 79~81% | 판례 조사는 AI 가 사람 위 | vals.ai 2025-10-14 | LIKELY |
| Stanford "Hallucination-Free?" | 검색증강 법률 AI 환각률 Lexis+ 17% · Westlaw AI-AR 33% · GPT-4 43% | 전문 DB 를 붙여도 6건 중 1건은 틀린 인용 | arXiv 2405.20362, JELS 게재 | FACT |
| **Harvey Legal Agent Benchmark (LAB)** — 1,250+ 과제, 전문가 채점 기준 75,000+ | 모든 기준 통과(All-Pass) 최고 7.1% (Claude Opus 4.7). 전 모델 10% 미만. 1회 실행 약 $50 · 22분 | **여러 단계를 이어 끝까지 하는 일은 10건 중 9건 어딘가 빠짐** — 우리 문서 "끝내기" 단계가 비어 있음 | harvey.ai 2026-05-26 | LIKELY(원문 표 미대조) |
| Legora BAR — 실제 사건 5,161건 | 절대 점수 비공개 | 비교용만 | legora.com 2026-09-10 | 참고 |
| 변호사 무작위 대조 실험 (Choi·Schwarcz) | 속도는 유의미하게 늘고 품질은 소폭·불규칙. 하위권이 가장 많이 늘고 상위권은 떨어지기도 | AI 는 초보를 끌어올리지 20년차를 만들진 않음 | Minnesota L. Rev. 109 / J. Legal Educ. 73 | LIKELY(정량 미확인) |
| 채택률 | 변호사 AI 사용 79% (Clio 2025) · ABA 30% (2025) · 전문가급 AI 없으면 입사 거절 36% (TR 2026) | 쓰는 건 보편, 맡기는 건 아님 | clio.com · abajournal · thomsonreuters.com | FACT / 2차 |

## 4. 나라별 — 무엇이 막고 무엇이 열렸나

| 나라 | 제품 (자율 정도) | 규제 사실 | 우리에게 뜻 | 확신도 |
|---|---|---|---|---|
| 한국 | 슈퍼로이어 (로앤컴퍼니) — 변호사 6,000명 (전체 20%), 롱폼 30장 서면 (2025-07), "슈퍼 에이전트" 공개 (2026-06), 아시아 9개 법역 LexPand AI (2026-09). 엘박스 3.0 검색→법리→문서 연결 (2026-07) | 변호사법 34조·109조 — 비변호사 유상 법률사무 금지. 대한변협 "AI 도 비변호사" (2024-05). **AI대륙아주 징계** 과태료 1,000만원 (2024-11). 로톡은 법무부 징계 취소 (2023-09)·공정위 과징금 취소 (2024-10) 로 정리. AI기본법 시행 2026-01-22 | 일반인 직접 상대는 막힘. **변호사가 고용주인 B2B 만 열림** — 슈퍼로이어가 이 길 | FACT |
| 일본 | LegalOn — 고객 7,000+, 연매출 100억엔, 에이전트 5종 (Triage 자동 승인·에스컬레이션, Draft). MNTSQ AI Agent (2025-10, 대형 로펌 감수 플레이북). Bengo4 Legal Brain Agent (2025-05) | 법무성 지침 (2023-08): 템플릿 표시는 적법, **법적 위험 판단 + 수정안 제시는 변호사법 72조 위반 소지**. 2026-08 개정판 언급 | 계약 AI 가 세계 최대인데 "판단" 은 선을 그어 둠 | FACT(회사) / LIKELY(지침 세부) |
| 중국 | 최고인민법원 — 2025년 전 법원 AI 배치 목표, 法信 유사판례 추천, 개별 법원 DeepSeek 도입. 通义法睿 (알리바바) 계약 심사·문서 생성 | AI 분쟁 첫 전국 사법규칙 (2026-09-07). 상업 제품 규모는 접근 차단으로 미확인 | 국가가 법원 안에서 먼저 씀 | LIKELY |
| 영국 | Garfield (SRA 인가 AI 로펌), Luminance, Juro Operator, Genie Agents (고객 20만+), Lawhive (사람 변호사 매칭) | **SRA 가 AI 로펌을 인가하는 길** (2025-05). SRA "AI 오용 경고" 신고 42건 (2026-08-17) | 규제기관이 문을 열어 준 유일한 나라 | FACT(SRA) |
| 미국 | 1~2절 대부분 | ABA 의견 512 (2024-07) 의무 6개 — 역량·비밀·소통·감독·법원 정직·합리적 수임료. 주별 AI 고지 규칙 (몬타나 필수 고지, 뉴욕·플로리다 인증). **Nippon Life v. OpenAI** (2026-03, ChatGPT 로 소송 서류 50건 = 무자격 법률행위인가, 진행 중). OpenAI 사용정책 — 전문가 감독 없는 법률 자문 금지 (2025-10-29). 환각 인용 제재 사례 DB 800~2,022건 (출처별 편차) | 서명·제출·일반인 자문 = 자격자 전속. 나머지는 열림 | FACT / LIKELY |
| EU | Noxtua (독), Doctrine (프) | AI Act 부속서 III 8(a) — 사법기관 보조 AI 는 고위험. 적용 2026-08-02 → 2027-12-02 로 연기 (Digital Omnibus, 2차 자료) | 법원용은 고위험, 로펌용은 아님 | FACT(조문) / LIKELY(연기) |
| 범용 모델사 | Claude for Legal (2026-05-12, 플러그인 12 · 연동 20) · Gemini Enterprise for Legal (2026-08-25, 출시 고객 Freshfields 등 4) · Microsoft Word Legal Agent (2026-05, 2차) · CoCounsel 이 Claude Agent SDK 위로 이사 | — | 전문 회사가 모델사 부품 위에 얹히는 구조로 굳어짐 | FACT / LIKELY |

## 5. 우리 정의 문서와 대조

### 5-1. "대체의 뜻" 으로 재면

| 우리 기준 | 남들 현황 | 판정 |
|---|---|---|
| 사람이 중간에 확인·고치면 아직 대체 아님 | 13개 제품 전부 "변호사 검토" 를 구조에 박음. EvenUp 은 사람 100명+ 가 뒤에서 재작성 | **대체 0건** |
| 사람 부르는 다섯 경우 (되돌릴 수 없음·승인 조건·판단 안 섬·한도 초과·자격자 전속) | Ironclad 3단계 게이트 = 한도 초과·승인 조건. Eve 체크포인트 = 승인 조건. 서명·제출·일반인 자문 = 자격자 전속 | 다섯 경우 중 셋은 이미 업계 관행. **"판단이 안 서서" 를 스스로 알고 부르는 장치는 아무도 공개 안 함** |
| 초보와 전문가를 가르는 5단계 (보기·알기·정하기·하기·끝내기) | 보기·알기는 변호사 위 (VLAIR 조사 81% vs 71%). 정하기·하기는 고쳐 쓰기에서 사람 아래. **끝내기는 LAB 7.1%** | 뒤 세 단계가 비어 있음 |

### 5-2. 9계통 재료 중 남들이 가진 것

| 계통 | 남들이 이미 가진 것 | 비어 있는 것 |
|---|---|---|
| 환경 | Word·이메일·계약관리·판례 DB 연결. MCP 표준화 (Harvey 커넥터, CourtListener MCP, iManage MCP) | 법원 전자소송 직접 제출은 없음 |
| 자료·검색 | Westlaw·Lexis·자체 600+ DB. Shepard's 인용 검증 | — |
| 지식·경험 | 플레이북 (Spellbook·Ironclad·MNTSQ 로펌 감수), 해결 사건 20만 건 학습 (EvenUp), 기관 기억 (Luminance·Eudia) | 20년차의 "정석·모르는 것" 을 명시한 지식체계는 없음 |
| 기억·상태 | Vault (Harvey), 사건 장부 (Supio) | — |
| 규칙·권한 | 위험도 게이트 (Ironclad), 체크포인트 (Eve), 불변 감사기록 | 임계값 공개 없음. "판단 안 섬" 감지 없음 |
| 행동 체계 | 워크플로 빌더 (Harvey 25,000개, Lexis 300+, Legora, Ironclad Act Mode) | 처음 보는 상황에서 길 찾기 = LAB 7.1% |
| 실무 | 계약·청구서·소장·조사 메모·의료 연표 | 송무 전 과정, 등기·인허가 없음 |
| 검증·평가 | 벤치마크 (VLAIR·BigLaw Bench·LAB·BAR), 인용 확인, 변호사 선호 비교 | **성과 지표 (유리 종결률·합의금·보정 횟수) 로 재는 곳이 없음** — 다 "시간 절감" 으로만 잼. EvenUp 합의금 69% 만 예외 (자체) |
| 학습·개선 | 공개된 것 거의 없음 | 결과로 배우는 고리 없음 |

### 5-3. 첫 직종 고를 때 참고

| 후보 자리 | 남들 성숙도 | 규제 | 성과 지표 재기 | 판정 |
|---|---|---|---|---|
| 기업 자문 (계약 검토·협상) | 가장 높음 (Luminance 자율 협상, LegalOn 7,000 고객) | 사내법무는 무자격 문제 없음. 일본은 "판단" 선 있음 | 분쟁 건수·검토 일수 — 잴 수 있음 | **가장 열려 있음** |
| 원고측 인신사고 (청구서→합의) | 높음 (EvenUp·Eve·Supio, 건 단위 위임형) | 로펌 안에서만 | 합의금·한도액 도달률 — 돈으로 바로 잼 | 위임형 + 성과 지표 둘 다 맞음. 미국 한정 |
| 소액 채권 회수 | Garfield 하나 | 영국은 인가로 열림. 한국은 34조 | 회수액·기간 | 나라 고르기가 관건 |
| 송무 (서면·제출) | 초안까지만 | 서명·제출 = 자격자 전속 | 유리 종결률 | 다섯 경우가 자주 켜짐 |
| 일반인 직접 상담 | DoNotPay 제재 | 한·미·일 다 막힘 | — | 제외 |

## 6. 못 확인한 것

- 정가 — 13개 제품 전부 비공개. 표의 가격은 제3자 추정이라 뺌 (Garfield 만 공개)
- CoCounsel·Legora·Protégé 신제품의 제3자 환각률 — Stanford 는 구제품만 잼
- 환각 인용 제재 DB 누적 건수 — 800~2,022건으로 출처마다 다름. 원사이트 접근 차단
- Harvey LAB 원문 표, Choi·Schwarcz 정량 수치 — 원문 접근 실패 (403)
- 한국 대한변협 단독 AI 지침 문서, AI대륙아주 이의신청 결과
- Arizona ABS·Utah 샌드박스 안 AI 법률 회사 — 검색 예산 소진으로 미조사
- 싱가포르·인도 (Intelllex·Lucio) — 실체 미확인

## 7. 출처 (확인일 2026-09-11)

| 대상 | URL |
|---|---|
| Harvey 에이전트·투자 | harvey.ai/platform/workflow-agents · harvey.ai/blog/introducing-harvey-agents · cnbc.com/2026/03/25 · harvey.ai/blog/connector-library |
| Harvey LAB · BigLaw Bench | harvey.ai/blog/legal-agent-benchmark-initial-results · harvey.ai/blog/biglaw-bench-hallucinations |
| Legora | cnbc.com/2026/03/10 · legora.com/blog/2026-the-year-of-agents-in-legal-ai · legora.com/bar |
| CoCounsel | thomsonreuters.com/en/press-releases/2025/august/…cocounsel-legal · …/2025/november/…agentic-ai · thomsonreuters.com/en-us/posts/innovation/rebuilding-for-the-agent-era |
| Lexis+ Protégé | lawnext.com/2026/02/lexisnexis-launches-lexis-with-protege · sec.gov RELX 6-K 2026-02-12 |
| Luminance | luminance.com/autonomous-negotiation · luminance.com/press/…series-c · cnbc.com/2023/11/07 |
| Ironclad | prnewswire.com …302614708 · ironcladapp.com/resources/articles/the-reality-of-ai-agents-in-legal-operations-today |
| Spellbook | betakit.com/spellbook-raises-50-million-usd-series-b · spellbook.com |
| EvenUp | fortune.com/2025/10/07 · evenuplaw.com/products/demands · slashdot.org/story/24/12/13 |
| Eve | eve.legal/blogs/introducing-eve-2-0 · legaltechnology.com/2025/09/30 · lawnext.com/2025/10 |
| Crosby | crosby.ai · artificiallawyer.com/2025/10/08 · legaltech.ca/2026/04/01 |
| Garfield | garfield.law |
| Robin AI | robinai.com/…series-b · fortune.com/2024/11/12 · v.daum.net/v/20251113070256470 |
| Supio · Eudia | supio.com/press/…series-b · prnewswire.com …302375331 · techcrunch.com/2024/08/27 |
| Vals VLAIR | vals.ai/industry-reports/vlair-2-27-25 · vals.ai/industry-reports/vlair-10-14-25 |
| Stanford 환각 | dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf |
| 채택률 | clio.com/about/press/clio-latest-legal-trends-report · thomsonreuters.com/en/institute/future-of-professionals-2026 |
| DoNotPay FTC | ftc.gov/news-events/news/press-releases/2025/02/ftc-finalizes-order-donotpay |
| ABA 512 | thebarexaminer.ncbex.org/article/fall-2024/generative-artificial-intelligence-tools |
| EU AI Act | artificialintelligenceact.eu/annex/3 |
| 한국 | fnnews.com/news/202410150855064221 · etnews.com/20250701000048 · lawtimes.co.kr …idxno=222131 · lawtimes.co.kr …idxno=204516 · anthropic.com/customers/law-and-company · law.go.kr 변호사법 |
| 일본 | legalontech.com/press-releases (7,000 고객 · 시리즈E · ARR) · moj.go.jp/content/001400675.pdf · mntsq.co.jp/news/release/mntsq-ai-agent-2025 |
| 중국 | english.court.gov.cn/2026-05/28/c_1187213.htm · help.aliyun.com/zh/model-studio/tongyi-farui |
| 영국 규제 | sra.org.uk/…/misuse-ai · sra.org.uk/news/news/releases/responsible-use-ai |
| 범용 모델사 | claude.com/solutions/legal · cloud.google.com/blog/…/introducing-gemini-enterprise-for-legal · wiki.free.law (CourtListener MCP) · imanage.com …mcp |
| 설계 재료 | harvey.ai/blog/enterprise-grade-rag-systems · lexisnexis.com …shepard-s-citation-validation · legal.thomsonreuters.com/blog/behind-the-build-of-the-next-generation-of-cocounsel-legal |

안이 어떻게 돌아가는지는 [바깥조사-법률-AI-에이전트-내부구조.md](바깥조사-법률-AI-에이전트-내부구조.md) 에 따로 뜯어 둠.
