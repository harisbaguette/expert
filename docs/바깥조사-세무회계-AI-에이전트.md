# 바깥 조사 — 세무·회계·기장 전문 AI 에이전트 (전 세계)

진행 계획 3단계 "바깥 조사 — 남이 만든 에이전트 비교" 의 **두 번째 직종군**임 (첫 번째는 법률). 확인일 2026-09-11. 검색 일꾼 6명이 모은 1차 자료를 부모가 대조해 씀. 확신도는 FACT(1차 자료 직접 확인) · LIKELY(2차 자료 또는 자체 발표만) · 미확인 으로 붙임.

## 한 줄 결론

법률과 다르게 **세무·회계는 "사람 없이 끝까지 한다" 고 대놓고 말하는 회사가 이미 여럿 나왔음** (Pilot "사람 개입 0", Black Ore "처음부터 끝까지 사람 거의 없이", Basis "법인 세금신고서 한 장 자율 완주 시연"). 그런데 **제3자가 재 보면 최고 모델이 미국 소득세 신고서를 제대로 계산해 내는 비율이 32% 밖에 안 됨** (TaxCalcBench). 즉 **자랑은 앞서 있고 실력은 아직 3분의 1** 이고, 그 틈을 회계법인 직원이 조용히 메우고 있음. 한국은 세무사법 제20조가 있어서 **AI 혼자 세무대리는 못 하고, 세무사가 데리고 쓰는 길만 열려 있음** — 이 길로 간 삼쩜삼은 4년 2개월 싸워 무혐의를 받았지만 2025년에 또 고발당함.

## 1. 지도 — 여섯 갈래

| 갈래 | 누가 쓰나 | 대표 제품 (나라) | 규모 (최신 발표) | 사람이 끼는 자리 |
|---|---|---|---|---|
| 소비자 직접 신고 | 일반인·프리랜서 | TurboTax·Intuit Assist (미), H&R Block AI Tax Assist (미), april (미), 삼쩜삼 (한), SSEM (한) | Intuit 연매출 $21.4B(+14%), TurboTax Live 매출 +37% (2026-08-25) / april 2026년 신고 140만 건 | **AI 가 채워 주고 사람이 최종 제출**. Intuit 은 오히려 사람 전문가(Live) 매출이 TurboTax 의 53% 로 커짐 |
| 세무법인용 신고 자동화 | 미국 회계법인(CPA firm) | Black Ore Tax Autopilot (미), Filed (미), Basis (미) | Black Ore 상위 20개 회계법인의 40% 사용 (2026-04) / Basis 기업가치 $1.15B, 상위 25개 법인의 약 30% (2026-02) | 회계사가 서명·제출. Black Ore·Basis 만 "사람 거의 없이" 를 내세움 |
| 세법 조사·판단 보조 | 세무사·세무변호사 | Blue J (캐), TaxGPT (미), CCH Axcess Advisor (Wolters Kluwer), Checkpoint Edge with CoCounsel (Thomson Reuters) | Blue J 시리즈D $122M, 2025 상반기 매출·고객 2배 (2025-08) | 답을 찾아 줄 뿐 신고서를 만들지 않음 |
| 기장·결산 자동화 | 스타트업·작은 회사 | Pilot (미), Digits (미), Puzzle (미), Truewind (미), Rillet·Campfire (미), freee·Money Forward (일), Xero JAX·Sage Copilot (영), 더존 ONE AI (한) | Rillet 기업가치 $1B·고객 600+ (2026-08) / 더존 ONE AI 누적 고객사 7,800곳+ (2026-09) | Puzzle·Rillet 은 "사람이 승인해야 장부에 올라감" 을 명시. Pilot·Digits 는 승인 단계를 아예 없앴다고 주장 |
| 감사 | 회계법인 감사팀·빅4 | DataSnipper (네), Fieldguide (미), MindBridge (캐), Trullion (이) | DataSnipper 2025년 고객 생산성 $1.4B 절감·175개국·빅4 전부 / Fieldguide 미국 상위 100대 법인 절반 사용 | **감사의견 서명은 회계사 전속.** AI 는 증빙 대조·위험 표시까지만 |
| 사람 기장사를 AI 로 바꾸려다 망한 곳 | — | Bench (캐, 2024-12 폐업), ScaleFactor (미, 2020 폐업) | Bench 누적 조달 $113M, 파산 신고 부채 $65M+ | ScaleFactor 는 "AI 라던 것이 사실은 해외 회계사 + 약간의 기술" 이었다는 폭로로 무너짐 |

관세사(통관·품목분류) 쪽은 검색 예산이 먼저 떨어져 못 봤음 — 6절에 적음.

## 2. 제품별 — 실제로 무엇을 스스로 하나

| 제품 | 스스로 하는 것 (기능명 · 출시) | 못 하는 것 · 사람 자리 | 성능 주장 (근거) | 확신도 |
|---|---|---|---|---|
| **Pilot** (미) | AI Accountant (2026-02-04) — 고객 받기·회계 설정·지난 장부 마감·예외 처리·재무제표 완성까지 한 줄로 이어감 | 공식 발표문에 사람 자리를 아예 안 적음. 다만 기존 상품은 "사람 컨트롤러가 매달 검토" 하는 방식도 같이 팜 | 원문 그대로 "from onboarding to monthly close, with **zero human intervention**". 10년간 7,000개 회사 기장 경험으로 학습. 정확도 수치는 없음. 몇 주 → 몇 시간 | FACT(주장 원문 확인) / 정확도 미확인 |
| **Black Ore** (미) | Tax Autopilot — 개인 소득세(1040) 준비를 서류 읽기부터 검토까지. 2026-04-29 대기자 공개 | 회계사가 서명·제출 | 원문 "complex tax workflows **from start to finish with little to no need for human intervention**". 시간 98% 절감·추출 정확도 99%+ 주장은 경쟁사 블로그가 옮긴 것이고 **제3자 검증 없다고 그 글이 스스로 적음** | FACT(기능) / LIKELY(수치) |
| **Basis** (미) | 회계법인용 에이전트 — 고객 자문·세무·감사 업무를 끝에서 끝까지. **법인(파트너십) 세금신고서 1065 를 자율로 완주하는 시연** 공개 | 회계법인 안에서만. 서명은 회계사 | 효율 20~50% 향상. 상위 25개 회계법인의 약 30% 가 씀 | FACT(투자·고객) / LIKELY(시연) |
| **Filed** (미) | 신고서 한 건의 전 과정 — 제각각인 고객 서류 정리 → 신고서 검증 → 법인이 정한 규칙으로 이상값 표시 (2025-05) | 회계사 검토·서명 | 고객 사례 "7일 → 하룻밤", "CPA 를 덜 쓰고 4배 처리". 자사 블로그 "TaxCalcBench 에서 줄 단위 94% 정확" — **그 벤치마크가 너그럽다고 스스로 적음** | FACT(기능·투자) / LIKELY(수치) |
| **Digits** (미) | Agentic General Ledger — 거래를 사람 손질 없이 바로 장부에 올림 | 홈페이지에 **사람이 봐야 하는 자리를 한 줄도 안 적음** | 1억 7천만 건·$875B 거래 학습. "회계 과제에서 일반 LLM 보다 43% 낫다" — 절대 정확도는 공개 안 함 | FACT(주장 원문 확인) |
| **Puzzle** (미) | 분류·대사·마감 준비를 AI 가 함 | 원문 "**사람 팀이 승인하기 전에는 아무것도 장부에 올라가지 않음**" | 누적 조달 $50M | LIKELY |
| **Rillet** (미) | AI 네이티브 ERP — 에이전트가 실시간 총계정원장 안에서 분석·대사·업무를 직접 함 (2026-08 시리즈C) | 원문 "**필요할 때는 사람 승인을 요구**", 감사 기록 유지 | 기업가치 $1B, 고객 600곳+, 3개월 만에 연매출 2배, EY 와 제휴 | FACT |
| **Truewind** (미) | 은행 거래 자동 분류, PDF 계약·청구서 읽어 분개(장부 한 줄) 자동 생성, 과거 입력에서 배움 | 회계법인이 검토 | 고객 100곳+·누적 $17.5M (2차 집계) | FACT(기능) / LIKELY(규모) |
| **Blue J** (캐) | Ask Blue J — 세법 질문에 근거 달린 답. 세법 판단 결과를 미리 맞혀 줌 | 신고서를 만들지 않음. 세무사가 판단 | 시리즈D $122M (2025-08), 2025 상반기 매출·고객 2배. "예측 정확도 90%" 주장 | FACT(투자) / LIKELY(정확도) |
| **TaxGPT** (미) | 세법 리서치·메모·고객 응대 초안 | 신고서 작성 안 함 — "리서치 보조" 로 스스로를 규정 | "적용 세법 인용 98.7% 정확" — 출처가 3자 리뷰 집계라 근거 불명 | LIKELY(성격) / 미확인(수치) |
| **Wolters Kluwer CCH Axcess** (미) | Advisor 정식 출시(2026-05-13), Workflow 에 AI 일정 추천(2026-05-05), Scan 이 K-1 같은 원천 서류를 읽어 "손 거의 안 대는 신고 준비" (2026-06-29) | 회계사 검토 | 수치 없음 | FACT(출시) |
| **DataSnipper** (네) | 감사 증빙 대조 자동화 — 숫자 하나하나를 원본 서류와 맞춰 표시 | 감사의견은 회계사 | 2025년 고객 생산성 $1.4B 절감, 175개국, 빅4 전부 사용 | FACT |
| **Fieldguide** (미) | 감사·자문 업무 에이전트 (2026-02 시리즈C $75M, 기업가치 $700M) | 감사의견 서명 | 미국 상위 100대 회계법인의 절반(빅4 포함)이 씀 | FACT |
| **MindBridge** (캐) | 거래 전수(표본 아님) 위험 분석 — 이상 거래를 점수로 매김 (2026-06 기능 확장) | 감사인이 판단 | 최근 투자액 못 찾음 | LIKELY |
| **freee** (일) | 세무사무소용 에이전트 4종 — 기장 / 규칙 정비 / 월차 점검 / **신고서 점검** (2026-08-07 공개, 9-15 유료 전환) | 세리사(일본 세무사)가 씀 — 세리사 사무소 전용 | 원문 "자료 회수부터 결산·신고까지 AI 로 한 흐름 지원" | FACT |
| **Xero JAX** (영) | 실시간 은행 대사, 영수증·청구서 읽어 자동 분류, 빠진 영수증 독촉, 지급 전 사기 점검 | 회계사·사업자 승인 | 전 세계 가입자 500만(영국 130만). Claude 연동 60일 만에 약 2만 고객 | LIKELY(3차 매체) |
| **삼쩜삼** (한) | 종합소득세 환급 신고 — 국세청 자료를 끌어와 환급액 계산·신고. "삼쩜삼 TA" 는 소득공제 항목·장부작성·경비분류를 AI 가 자동 수행 | **세무사 명의로 신고함.** 세무사회는 그 지휘·감독이 형식적이라고 고발 | 환급액 조회자 대비 환급 대상 71% (자사 집계) | FACT(고발 내용) / LIKELY(자사 수치) |
| **더존비즈온 ONE AI** (한) | 회계·세무·노무 국내 법령·실무를 학습한 버티컬 AI 가 반복 실무를 스스로 판단해 처리 | 기업 담당자 검토 | 2024년 출시 이후 누적 7,800개 기업 고객 (2026-09-02) | FACT |
| **SSEM(쌤)** (한) | 거래 내역·거래처를 분석해 계정 용도·부가세 공제 대상을 자동 판정, 부가세 신고 (2025-01 개시) | 세무사 확인 | "세금 신고 과정의 80% 자동화" (자사) | LIKELY |

제외(단순 챗봇·요약 도구라 지도에서 뺌): H&R Block AI Tax Assist(질문 답변만), 국세청 AI 전화상담(안내만), 세무통(세무사 매칭·상담 앱).

## 3. 진짜 실력 — 제3자 증거

| 무엇을 재나 | 결과 | 뜻 | 출처 · 날짜 | 확신도 |
|---|---|---|---|---|
| **TaxCalcBench** — 미국 개인 소득세 신고서를 실제로 계산시켜 채점 | 원문 "최신 모델들이 연방 소득세 신고서의 **3분의 1도 못 맞힘**". Gemini 2.5 Pro 32.35% · Claude Opus 4 27.45% · Gemini 2.5 Flash 25.98% · Claude Sonnet 4 23.04% | **세무의 "끝내기" 가 비어 있다는 가장 강한 증거.** 신고서는 한 줄만 틀려도 전부 틀림 | arXiv 2507.16126, 2025-07 (본문 표 직접 확인) | FACT |
| TaxCalcBench 오류 유형 | 세금표를 안 쓰고 세율로 계산 15~20%. 나머지는 서식 줄번호 착각·빈곤선 잘못 적용·공식 선택 오류 | 틀리는 이유가 "법을 몰라서" 가 아니라 **정해진 절차를 안 지켜서** 임 | 같은 논문 | FACT |
| **Vals TaxEval v2** — 세무 전문가가 만들고 두 번 검수한 문제 1,223개 | 페이지에 적힌 최고 기록이 답변 정확도 **68.03%** (단계별 추론은 92.72%) | 말로 답하는 세무 질의도 3문제 중 1문제는 틀림 | vals.ai/benchmarks/tax_eval_v2, 2026-09-01 갱신 | FACT(페이지 확인) / 전체 순위표는 그림이라 미추출 |
| **GAO 감사 보고서 — 국세청(IRS) 의 AI 사용** | 활성 AI 사용 사례 126건 (2022-08 에는 10건). **4분의 1 넘는 사례가 "이게 기관에 무슨 도움이 되는지" 조차 안 적혀 있음.** 77건(61%)은 아직 개발 중 | 세금 걷는 정부 기관조차 AI 를 관리 못 하고 있음. 권고 8건 전부 IRS 가 받아들임 | gao.gov/products/gao-26-107522, 2026-03-24 | FACT |
| **PCAOB(미국 상장사 감사 감독기구) 관찰 보고** | 원문 "현재 감사에서의 생성형 AI 활용은 **주로 행정·조사 업무에 집중**", 위험을 막으려면 강한 감독이 필요 | 감독기구가 본 실제 현장은 "판단" 까지 안 갔음 | pcaobus.org 2024-07-22 | FACT (2025~2026 후속 문서는 못 찾음) |
| **미국 조세법원 판결 Clinco v. Commissioner** (T.C. Memo. 2026-16) | AI 가 지어낸 가짜 판례 인용이 납세자 주장을 무너뜨림. 약 230만 달러 불일치가 걸린 사건 | 법정에서 AI 환각이 실제로 돈을 잃게 만든 첫 세무 사례 | 2026년, 2차 보도 | LIKELY |
| **IRS 직업윤리실(OPR) AI 지침** | 원문 취지 "세무대리인은 자기 일의 정확성에 **전적으로 책임**", "**AI 때문에 틀렸다는 별도 범주도, 알고리즘 결과를 믿었다는 면책도 없다**" | 미국은 "AI 가 틀렸다" 가 변명이 안 됨을 못 박음 | Thomson Reuters 세무뉴스, 2026년 | LIKELY |
| **GhostCite** — LLM 13종의 인용 신뢰도 | 환각률 14.23%(DeepSeek) ~ 94.93%(Hunyuan) | 근거 대는 능력이 모델마다 7배 차이 남 | arXiv 2602.06718, 2026-05-15 (표 원문 추출 실패) | LIKELY |
| FinanceBench — 상장사 재무 질의 | GPT-4-Turbo + 검색 붙여도 81% 를 틀리거나 답을 거부 | 오래된 결과(2023-11)라 참고만 | arXiv 2311.11944 | 참고 |
| **Bench 폐업** (캐, 기장 대행) | 2024-12-27 예고 없이 폐업 → 12-30 Employer.com 인수. 누적 조달 $113M, 2025-01 캐나다 파산 신청 부채 $65M+ | 사람 기장사를 싸게 쓰던 모델은 무너짐 | techcrunch.com 2024-12-30 | FACT |
| **ScaleFactor 폭로** (미) | 약 $100M 조달 뒤 2020 폐업. "AI 기장" 이라던 것이 **사실은 해외 회계사 + 약간의 기술** 이었음이 드러남 | 이 업계의 "사람이 뒤에서 한다" 전형 | 2차 업계 블로그 (원 폭로 기사 원문 미확인) | LIKELY |

**반대 증거 한 바퀴 결과**: Pilot·Digits·Basis·Black Ore 를 지목한 개별 폭로·제재·소송은 **찾아봤지만 없었음**. 대신 같은 업계의 선배격인 ScaleFactor·Bench 가 실제로 무너진 기록이 있고, 제3자 벤치마크 수치(32%·68%)가 이들의 자체 주장(99%·"사람 개입 0")과 크게 어긋남.

## 4. 나라별 — 무엇이 막고 무엇이 열렸나

| 나라 | 제품 (자율 정도) | 규제 사실 | 우리에게 뜻 | 확신도 |
|---|---|---|---|---|
| **한국** | 삼쩜삼(환급 신고, 세무사 명의) · SSEM(부가세 80% 자동) · 택스비(기장 연 200만원→12만원 표방, 2023) · 더존 ONE AI(기업 7,800곳) · 국세청 AI 전화상담(2025-05-01~06-02 시범, 종합소득세·장려금, AI 뒤 직원 연결) | **세무사법 제20조 제1항 "제6조에 따른 등록을 한 자가 아니면 세무대리를 할 수 없다"**. 제2조가 세무대리 8가지를 정해 둠. 어기면 **제22조 3년 이하 징역 또는 3천만원 이하 벌금**. 현행 시행 2026-06-24(법률 제21220호). **삼쩜삼 1차 고발(2021-03) → 경찰 불송치(2022-08) → 검찰 불기소(2023-11) → 항고·재항고 기각(2025-05-29) 으로 4년 2개월 만에 무혐의 확정.** 그런데 2025-05-30 세무사회가 **4차 고발** — "삼쩜삼 TA 는 세무사의 직접 개입 없이 소득공제·장부작성·경비분류를 AI 가 자동 수행하며, 세무사의 지휘·감독은 형식적이거나 존재하지 않는 것으로 보인다". 개인정보위 과징금 8억 5,410만원+과태료 1,200만원(2023-06-28), 공정위 과장광고 과징금 7,100만원(2025-12) | **AI 혼자 세무대리는 막힘. 세무사가 이름을 걸고 데리고 쓰는 길만 열림** — 그런데 그 "데리고 쓴다" 가 얼마나 실질적이어야 하는지가 지금 다투는 지점임. 우리 문서의 "자격자 전속" 경우가 여기서 정확히 켜짐 | FACT(사건) / LIKELY(조문 문구는 위키문헌 판본 기준) |
| **미국** | 2절 대부분 + TurboTax·H&R Block·april. IRS Direct File 은 2026 신고 시즌에 **없음** ("Direct File is closed") | **Circular 230** — 국세청 앞에서 대리할 수 있는 사람은 변호사·공인회계사·등록세무사(EA) 뿐. **PTIN 규정** "보수를 받고 연방 신고서를 작성하거나 작성을 돕는 자는 누구든 유효한 2026 PTIN 이 있어야 함" — PTIN 은 **사람 앞으로만** 나옴. AI 명의 발급 조항 없음 | 신고서에 이름을 올리는 자리는 사람 전속. 그 앞 단계는 전부 열려 있어서 Black Ore·Basis·Filed 가 거기서 큼 | FACT |
| **일본** | freee 에이전트 4종(세리사 사무소 전용), Money Forward AI 확정신고(2025-11) | **세리사법 제52조 "세리사 또는 세리사법인이 아닌 자는… 세리사 업무를 해서는 안 된다"**. 어기면 2년 이하 구금형 또는 100만엔 이하 벌금 (국세청 안내). 일본세리사회연합회가 AI 이용 가이드라인 제정(2026-03, 법적 구속력 없음) — 입력 데이터 익명화, 최종 판단 책임은 세리사, 고객에게 AI 사용 설명 | 한국과 똑같은 구조. **그래서 freee 가 "세리사 사무소용" 으로만 파는 것** | FACT(조문) / LIKELY(가이드라인) |
| **영국** | Xero JAX, Sage Copilot(Finance Intelligence Agent 2026 하반기 정식), Dext | **2026-04-06 부터 소득 5만 파운드 초과 개인사업자·임대인에게 디지털 세무(MTD) 의무화.** HMRC 는 2026년부터 AI·데이터 분석으로 세무 조사를 강화하겠다고 함. 세무대리인 HMRC 등록 의무화 추진 | **국가가 먼저 장부를 디지털로 강제** → AI 기장이 자랄 땅이 만들어짐 | LIKELY(3차 매체) |
| **중국** | 金蝶(Kingdee) 기업 AI 운영체제 "灵基(Lingee)" 발표(2026-05-20) — AI 재무부가 비용 심사·지능 대사·보고서 작성 등 6대 응용 | 접근 차단으로 세무총국 방침·航天信息·用友 는 미확인 | 재무를 "사후 기장" 에서 "실시간 중추" 로 바꾸겠다는 방향만 확인 | LIKELY |
| **EU** | — | **AI Act 부속서 III 고위험 8개 항목을 직접 열어 확인한 결과 "tax"·"taxation"·"tax authorities" 라는 말이 한 번도 안 나옴.** 신용평가만 5(b) 에 있음. 부속서 III 고위험 의무는 2027-12-02 부터 | **세무·회계 AI 는 EU 고위험 목록 밖** — 법률(사법 보조)보다 오히려 규제가 느슨함 | FACT(조문 직접 확인) |
| 빅4 | EY.ai 에이전트 플랫폼("디지털 세무 담당자 150명" 배치, 세무 인력 8만 명 → 2028년 10만 명), PwC Agent OS(에이전트 2.5만 개), Deloitte Zora AI, KPMG 20억 달러 투자 | — | **가장 큰 돈은 빅4 안에서 움직임.** 우리가 그 자리를 뺏는 건 아님 | LIKELY(3차 매체) |

## 5. 우리 정의 문서와 대조

### 5-1. "대체의 뜻" 으로 재면

| 우리 기준 | 남들 현황 | 판정 |
|---|---|---|
| 사람이 중간에 확인·고치거나 마무리하면 아직 대체 아님 | Puzzle "승인 전엔 장부에 안 올라감", Rillet "필요할 때 사람 승인", Filed·Black Ore·Basis 는 회계사 서명 전제. **Pilot·Digits 둘만 "사람 자리 없음" 을 내세움** | **대체를 주장하는 곳이 2곳 생겼음** (법률은 0곳이었음) |
| 그 주장이 진짜인가 | 제3자 수치는 신고서 32%·세무 질의 68%. Pilot·Digits 는 **절대 정확도를 공개하지 않음** (Digits 는 "다른 LLM 보다 43% 낫다" 는 상대값만) | **자체 주장은 있고 제3자 검증은 0건** → LIKELY(자체) 를 못 넘음 |
| 사람 부르는 다섯 경우 | 자격자 전속(한국 세무사법 20조·일본 세리사법 52조·미국 PTIN)은 세 나라 다 켜져 있음. 승인 조건(Puzzle·Rillet), 되돌릴 수 없음(제출·서명)도 업계 관행 | 다섯 중 셋은 이미 관행. **"판단이 안 서서" 를 스스로 알고 멈추는 장치는 세무에서도 아무도 공개 안 함** |
| 5단계 (보기·알기·정하기·하기·끝내기) | 보기(서류 읽기)는 정확도 99% 주장까지 옴. 알기(세법 찾기)는 Blue J·TaxGPT. 정하기(공제 판단)는 SSEM·Black Ore. **끝내기(신고서 숫자를 끝까지 맞게)는 TaxCalcBench 32%** | **법률과 똑같이 "끝내기" 에서 무너짐.** 다만 세무는 끝내기가 숫자라서 **기계가 채점할 수 있다** 는 점이 다름 |

### 5-2. 9계통 재료 중 남들이 가진 것

이 계통별 요약은 조사 당시의 분류로 남긴다. 2026-09-11 재배치 후 현재 소속과 책임 경계는 [재료 정본](materials.md)과 [배치 검토](reviews/material-system-placement-review.md)를 따른다.

| 계통 | 남들이 이미 가진 것 | 비어 있는 것 |
|---|---|---|
| 환경 | 회계 프로그램·은행 계좌·카드·영수증 앱 연결 (Xero JAX 실시간 은행 대사, freee 자료 회수, 더존 ONE AI 국내 ERP). 미국 e-file 전자제출 인가(april 이 15년 만에 받은 11번째) | **한국 홈택스 직접 신고 제출 권한을 AI 이름으로 가진 곳 없음** (세무사 명의를 빌리는 구조) |
| 자료·검색 | 세법 DB (Blue J, CCH AnswerConnect, Checkpoint Edge), 국세청 연계 자료 (삼쩜삼) | — |
| 지식·경험 | 해결 사례 학습 (Digits 1억 7천만 건·$875B, Pilot 7,000개 회사 10년치) | **20년차 세무사의 "이건 조사 나온다" 같은 위험 감각을 적어 둔 지식체계 없음** |
| 기억·상태 | 총계정원장 자체를 AI 가 쥠 (Digits·Rillet) — 법률의 "사건 장부" 보다 진도가 빠름 | — |
| 규칙·권한 | 승인 게이트 (Puzzle "승인 전 반영 안 함", Rillet "필요 시 사람 승인"), 감사 기록 유지 (Rillet) | **임계값 공개 없음. Pilot·Digits 는 게이트가 있는지조차 안 밝힘** |
| 행동 체계 | 신고서 한 건 전 과정 (Filed), 1065 자율 완주 시연 (Basis), 기장→마감→재무제표 (Pilot), 에이전트 4종 분업 (freee) | 처음 보는 세법 상황에서 길 찾기 = TaxCalcBench 32% |
| 실무 | 개인 소득세·부가세·기장·결산·감사 증빙 대조·세법 조사 | **상속·증여·가업승계, 세무조사 대응, 불복(이의신청·심판청구), 관세·통관은 아무도 안 함** |
| 검증·평가 | 제3자 벤치마크가 **법률보다 잘 갖춰져 있음** (TaxCalcBench 는 신고서를 줄 단위로 채점, TaxEval v2 는 전문가 이중검수 1,223문항). 감사 쪽은 PCAOB 관찰 보고 | **우리 성과 지표로 재는 곳은 사실상 없음** — 아래 따로 |
| 학습·개선 | Truewind "과거 입력에서 배움" 정도만 공개 | 결과(가산세가 났는지)로 배우는 고리 없음 |

**성과 지표로 재는가 — 판정: 거의 없음.**

| 우리 직종표의 성과 지표 | 이 지표로 재는 곳 | 판정 |
|---|---|---|
| 신고 정확성 (수정신고·가산세 건수) | 없음. 대신 **TaxCalcBench 가 신고서 줄 단위 정확도를 잼** — 제품이 아니라 학계가 잼 | **제품은 안 잼, 벤치마크만 잼** |
| 기한 준수율 | 없음 | 없음 |
| 법 안에서 줄인 세액 · 환급액 | **삼쩜삼의 "환급 대상자 비율 71%" 가 유일하게 돈으로 잰 수치** (자사 집계) | 1곳뿐, 자체 발표 |
| 세무조사 지적률 · 불복 인용률 | **없음.** 조사·불복을 하는 AI 자체가 없음 | 없음 |
| 감사의견과 실제 결과 일치 (적정 의견 뒤 상장폐지·정정) | 없음. DataSnipper·Fieldguide 모두 시간·생산성만 잼 | 없음 |
| 월 마감 날수 · 대사 완료율 100% | 시간은 다 잼 (Filed 7일→하룻밤, Pilot 몇 주→몇 시간, Basis 20~50%, DataSnipper $1.4B). **대사 완료율 100% 를 내건 곳은 못 찾음** | **전부 "시간 절감" 으로만 잼** |

### 5-3. 첫 직종 고를 때 참고

우리 첫 직종 후보가 **세무사(신고·기장)** 라서 특히 자세히 봄.

| 후보 자리 | 남들 성숙도 | 규제 (한국) | 성과 지표 재기 · 기계 채점 가능성 | 판정 |
|---|---|---|---|---|
| **세무사 (신고·기장)** | **가장 높음** — Black Ore·Filed·Basis·Pilot 이 이미 "사람 거의 없이" 를 내세움. 한국도 삼쩜삼·SSEM 이 있음 | 세무사법 20조로 **AI 단독 불가**. 세무사 명의로만 가능하고, 그 감독이 형식적이면 지금도 고발당함(2025-05 4차) | **가장 잘 잼** — 가산세·수정신고는 국세청이 자동으로 매기는 숫자이고, 기한 준수는 날짜라 기계가 바로 채점함. TaxCalcBench 처럼 줄 단위 채점 틀도 이미 있음 | **남들이 제일 앞서 있지만 아직 32% 라 끝내기가 비어 있음. 우리 "기계가 끝났는지 확인" 조건을 가장 자연스럽게 만족함** |
| **기장 대행** | 높음 (Pilot·Digits·Puzzle·Truewind·더존) | 기장 자체는 세무대리에 걸리는 범위를 따져야 함 (세무사법 2조) | **대사 완료율 100% 는 기계가 그 자리에서 채점 가능** — 통장 잔액과 장부가 맞는지는 참·거짓이 딱 떨어짐 | **기계 채점이 가장 확실한 자리.** 다만 Bench·ScaleFactor 가 망한 자리이기도 함 |
| 세무사 (상속·증여·가업승계) | **없음 — 아무도 안 함** | 세무사 전속 | 설계 전후 세액 차이로 잼. 다만 결과가 몇 년 뒤 나옴 | 빈자리이지만 **되돌릴 수 없는 행동**이 자주 켜짐 |
| 세무사 (조사·불복) | **없음 — 아무도 안 함** | 세무사 전속 | **조세심판 인용률 27.3%(2024)라는 공개 기준선이 이미 있음** — 우리 성적을 바로 비교 가능 | 빈자리 + 성과 지표가 명확. 대신 건수가 적음 |
| 회계사 (감사) | 빅4 + DataSnipper·Fieldguide 가 이미 큼 | **감사의견 서명 = 자격자 전속** | 적정 의견 뒤 상장폐지 여부로 잼 — 결과가 몇 년 뒤 | **우리 자리 아님** (돈도 선수도 이미 다 있음) |
| 관세사 | 미조사 | — | — | 6절 |

**첫 직종에 대한 시사점 세 줄**
1. 세무 신고·기장은 **남들이 "다 했다" 고 말하면서 실제로는 3분의 1밖에 못 하는 자리** — 자랑과 실력의 틈이 제일 크게 벌어져 있음.
2. 세무는 **끝이 숫자라서 사람이 아니라 기계가 끝났는지 확인할 수 있음** — 우리 "대체의 뜻" 의 마지막 조건(기계 확인 + 기록)을 만족시키기에 법률보다 훨씬 유리함.
3. 한국에서 하려면 **세무사가 이름을 걸되 감독이 형식적이지 않게 만드는 장치** 를 처음부터 설계에 박아야 함. 삼쩜삼 4차 고발이 정확히 그 지점을 찔렀음.

## 6. 못 확인한 것

- **관세사(통관·품목분류·FTA 특혜관세) 분야 전체** — 검색 예산이 먼저 떨어져 한 곳도 못 봄. 제품 후보를 한 개 찍어 열어 봤지만(zonos.com/products/classify) 404 였음. 다음 조사에서 따로 봐야 함
- **한국 세무사법 조문 원문** — law.go.kr 이 자바스크립트로 본문을 그려서 WebFetch·curl·CDP 세 방법 다 실패함. 조문 문구는 위키문헌의 2009년 전문개정 판본(법률 제9348호)에서 가져왔고, 현행이 2026-06-24 시행 법률 제21220호 라는 사실만 law.go.kr 메타데이터로 확인함 → 문구가 그 사이 바뀌었을 가능성 남음
- **Pilot·Digits 의 절대 정확도** — 둘 다 "사람 없이 한다" 고만 하고 숫자를 안 냄. 제3자 검증도 없음
- **Vals TaxEval v2 전체 순위표** — 그림으로만 그려져 있어 모델별 수치를 못 뽑음. 페이지에 글자로 적힌 68.03% 하나만 확보
- **GhostCite 논문 원문 표** — PDF 글자 추출 실패, 검색 요약의 수치(14.23~94.93%)만 씀
- **세친구·알밤·이카운트** — 위임문에 후보로 있었으나 검색에서 세무 AI 제품으로서 아무것도 안 나옴. 실체 미확인
- **국세청 AI 상담 처리 건수**, 홈택스 AI 상담이라는 별도 서비스의 존재 — 국세청 보도자료가 한글 첨부파일이라 못 읽음
- **중국 航天信息(Aisino)·用友(Yonyou)·국가세무총국 AI 방침** — 예산 소진으로 검색 못 함. Kingdee 도 1차 페이지 본문 확인 실패
- **Money Forward IR 수치**(유료 사용자·매출), **Sage Copilot 사용자 수**, **Trullion 투자액·고객 수**, **MindBridge 최근 투자액** — 전부 못 찾음
- **빅4 AI 발표의 공식 뉴스룸 원문** — 3차 매체 취합글만 확보. KPMG 공식 페이지는 404
- **PCAOB 의 2025~2026 후속 AI 지침** — 존재한다는 2차 언급만 있고 원문 링크를 못 찾음
- **FTC 의 TurboTax 광고 제재가 2026년 현재도 유효한지** — 원 보도자료 URL 이 404
- 회계·세무에 한정한 **환각률 학술 연구** — 법률 쪽(Stanford)처럼 딱 맞는 논문을 못 찾음

## 7. 출처 (확인일 2026-09-11)

| 대상 | URL |
|---|---|
| Intuit FY2026 실적 | investors.intuit.com/news-events/press-releases/detail/1320 (2026-08-25, 본문 직접 확인) |
| H&R Block AI Tax Assist | investors.hrblock.com/news-releases/news-release-details/hr-block-combines-ai-power-digital-enhancements-and-unmatched |
| april · Column Tax | businesswire.com/news/home/20260827184313 · columntax.com |
| IRS Direct File 중단 | irs.gov (Direct File 안내), 2차 보도 Tax Notes·Forbes 2025-11 |
| IRS Circular 230 · PTIN | irs.gov/tax-professionals/circular-230-tax-professionals (2026-05-28 갱신) · irs.gov/tax-professionals/ptin-requirements-for-tax-return-preparers (2025-10-16 갱신) |
| IRS OPR AI 지침 | tax.thomsonreuters.com/news/irs-office-of-professional-responsibility-issues-guidelines-on-ai-use-in-tax-practice |
| Clinco v. Commissioner | T.C. Memo. 2026-16 (2차: aiolacpa.com/when-ai-goes-to-tax-court-and-loses) |
| Black Ore | blackore.ai/news (2026-04-29) · blackore.ai/post/black-ore-emerges-from-stealth-with-60-million-funding |
| Filed | cpapracticeadvisor.com/2025/05/21/…/161468 · filed.com/blog/best-ai-tax-prep-platforms |
| Basis | cpapracticeadvisor.com/2026/02/24/basis-raises-100-million-to-deploy-ai-agents-for-accounting-firms/178759 · siliconangle.com/2026/02/24 |
| Blue J | internationalaccountingbulletin.com/news/blue-j-secures-122m-funding (2025-08-05) · ohiocpa.com/…/2026/02/12 |
| TaxGPT | g2.com/products/taxgpt/reviews (3자 집계) |
| Wolters Kluwer CCH Axcess | wolterskluwer.com/en/news/wolters-kluwer-launches-cch-axcess-advisor (2026-05-13) · …/wolters-kluwer-enhances-cch-axcess-workflow (2026-05-05) · …/wolters-kluwer-expands-cch-axcess-expert-ai (2026-06-29) |
| Thomson Reuters Checkpoint Edge | thomsonreuters.com/en/press-releases/2024/july/thomson-reuters-launches-new-ai-assisted-research-skill |
| Pilot AI Accountant | pilot.com/blog/pilot-unveils-ai-accountant-a-major-leap-toward-artificial-general-intelligence-in-accounting (2026-02-04, 본문 직접 확인) |
| Digits | digits.com (본문 직접 확인) |
| Puzzle · Truewind | puzzle.io/blog/puzzle-vs-digits · ycombinator.com/launches/I6w-truewind-ai-powered-bookkeeping-and-finance-software-for-startups |
| Rillet · Campfire | pulse2.com/rillet-raises-100-million-series-c-at-1-billion-valuation-as-ai-native-erp-tops-600-customers (2026-08-18) · erpscorecard.com |
| Bench 폐업 | techcrunch.com/2024/12/30/bench-to-be-acquired-after-abruptly-shutting-down · geekwire.com/2024/bench-accounting-to-be-acquired-by-employer-com |
| ScaleFactor | basis365.com/blog/why-bookkeeping-ai-services-keep-shutting-down (2차) |
| DataSnipper | prnewswire.com/news-releases/datasnipper-delivers-1-4b-in-productivity-savings-in-2025-…-302661257 (2026-01-14) |
| Fieldguide | fieldguide.com/blog/series-c-announcement (2026-02-02) |
| MindBridge · Trullion | mindbridge.ai/news/mindbridge-expands-audit-assurance-platform-… (2026-06-08) · trullion.com/blog/best-ai-audit-software |
| 빅4 감사 AI | financial-world.org/news/news/financial/30088 · chatfin.ai/blog/big-4-ai-agents-ey-kpmg-deloitte-pwc-finance-teams-2026 (3차) |
| PCAOB | pcaobus.org/news-events/news-releases/news-release-detail/pcaob-staff-shares-observations-from-outreach-on-use-of-generative-artificial-intelligence-in-audits-and-financial-reporting (2024-07-22) |
| TaxCalcBench | arxiv.org/abs/2507.16126 · arxiv.org/html/2507.16126v1 (표 직접 확인) |
| Vals TaxEval v2 | vals.ai/benchmarks/tax_eval_v2 (2026-09-01 갱신) |
| GhostCite | arxiv.org/pdf/2602.06718 (2026-05-15) |
| FinanceBench | arxiv.org/abs/2311.11944 |
| GAO — IRS 의 AI | gao.gov/products/gao-26-107522 (2026-03-24) |
| 삼쩜삼 무혐의 확정 | hankyung.com/article/2025061216861 (2025-06-12, 대검 결정 2025-05-29) |
| 삼쩜삼 4차 고발 | sejungilbo.com/news/articleView.html?idxno=53358 (2025-05-30, 본문 직접 확인) |
| 삼쩜삼 개인정보위 제재 | digitaltoday.co.kr/news/articleView.html?idxno=480193 (의결 2023-06-28) |
| 삼쩜삼 공정위 제재 | taxtimes.co.kr/news/article.html?no=275342 |
| SSEM · 택스비 | aitimes.com/news/articleView.html?idxno=167161 · byline.network/2025/01/22-390 · news.mt.co.kr/mtview.php?no=2023070716072070865 |
| 더존 ONE AI | taxtimes.co.kr/news/article.html?no=276669 (2026-09-02) |
| 국세청 AI 전화상담 | nts.go.kr/nts/na/ntt/selectNttInfo.do?mi=2207&nttSn=1342259 |
| 세무사법 | law.go.kr/법령/세무사법 (시행 2026-06-24, 법률 제21220호 — 메타데이터만) · ko.wikisource.org/wiki/세무사법_(대한민국) (조문 문구) |
| 일본 세리사법 52조 | nta.go.jp/taxes/zeirishi/zeirishiseido/qa/06.htm · laws.e-gov.go.jp/document?lawid=326AC1000000237 |
| 일본세리사회연합회 AI 지침 | kaikei-ai.jp/daily/2026-03-12 (3차) |
| freee | corp.freee.co.jp/news/20260807freee_AIagent&fAH.html (2026-08-07, 본문 직접 확인) |
| Money Forward | corp.moneyforward.com/news/release/corp/20250402-mf-press-1 · …/service/20251215-mf-press-1 |
| Xero JAX | thefirm.media/articles/xerocon-london-2026-announcements-what-actually-matters (2026-07-21) |
| Sage Copilot | sage.com/investors/investor-downloads/press-releases/2026/04/sage-expands-ai-agents-across-finance-hr-and-operations-to-automate-workflows |
| 영국 MTD · HMRC AI | icaew.com/insights/tax-news/2026/apr-2026/hmrc-clarifies-position-on-making-tax-digital-and-cessations · kpmg.com/uk/en/insights/tax/hmrc-2026-transformation-roadmap.html |
| Kingdee 灵基 | kingdee.com/kais2026 · kingdee.com/resources/articles/1507043088034809953 (2026-05-20) |
| EU AI Act 부속서 III | artificialintelligenceact.eu/annex/3 (본문 직접 확인) |
