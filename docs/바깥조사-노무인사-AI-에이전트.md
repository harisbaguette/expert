# 바깥 조사 — 노무·인사·채용 전문 AI 에이전트 (전 세계)

진행 계획 3단계 "바깥 조사 — 남이 만든 에이전트 비교" 의 직종군 하나임 (법률 다음). 확인일 2026-09-11. 검색 일꾼 7명이 모은 1차 자료를 부모가 대조해 씀. 확신도는 FACT(1차 자료 직접 확인) · LIKELY(2차 자료 또는 자체 발표만) · 미확인 으로 붙임.

## 한 줄 결론

법률과 정반대 모양임. **채용 쪽은 사람 없이 AI 가 면접을 보고 점수까지 매기는 자리가 이미 열렸고**(HireVue·Eightfold·Alex·Mercor), **급여·노무 쪽은 "에이전트" 라고 이름만 붙었지 전부 알려 주기까지만 하고 실행은 사람 승인**임 — Deel 이 내놓은 에이전트 7개는 하나도 빠짐없이 "추천한다·미리 표시한다" 로만 적혀 있고, Rippling 은 대놓고 "급여를 당신 승인용으로 차려 놓는다" 고 씀. 그리고 **30개를 다 뒤졌는데 우리가 보는 성과 지표(입사 뒤 잔존율·노동위 인용률·산재 승인율·급여 오류 0건)로 재는 곳은 한 곳도 못 찾았고, 전부 "몇 시간 아꼈다" 로만 잼**. 대신 규제는 법률보다 훨씬 촘촘함 — 채용 AI 는 EU 고위험·한국 고영향·뉴욕 감사 의무에 다 걸리고, **AI 만든 회사 자신이 피고가 된 전국 집단소송(Mobley v. Workday)이 이미 돌아가는 중**임.

## 1. 지도 — 여섯 갈래

| 갈래 | 누가 쓰나 | 대표 제품 (나라) | 규모 (최신 발표) | 사람이 끼는 자리 |
|---|---|---|---|---|
| 급여·노무 통합 플랫폼 | 회사 인사팀 | Rippling·Gusto·Deel·ADP·Paylocity·Workday (미), SmartHR·freee (일), Personio (독)·Factorial (스)·HiBob (영), 플렉스·시프티·자버 (한) | Rippling 연매출 환산 $1B·기업가치 $16.8B (2026-03) / Deel 기업가치 $17.3B·고객 37,000+·연 급여 $22B 처리 (2025-10) / ADP 고객 110만+ · 140개국 (2026-09) | **급여 지급·세금 신고 실행은 전부 사람 승인.** Rippling 원문 "stages the payroll run for your approval" |
| AI 면접관 | 대량 채용하는 회사 | HireVue·Eightfold·Alex·SeekOut Sam (미), Moka Eva (중), 마이다스 inAIR (한) | Alex 투자 $20M·누적 면접 100만+ (2025-09) / Eightfold 채용 주기 42일→1주 주장 (2026-07) | **면접 진행·채점까지 AI 혼자.** 사람은 ① 후보자 동의 받기 ② 최종 라운드 ③ 뽑을지 결정 |
| 채용 접수·소싱 에이전트 | 현장직 대량 채용·헤드헌팅 | Paradox(Olivia, Workday 가 인수), Juicebox, Moonhub (미), 원티드 채용 에이전트·그리팅 (한) | Workday 가 Paradox 인수 완료 2025-10-01 (금액 비공개) / 그리팅 기업 10,000+ | 후보 제안까지. 연락·오퍼는 사람 |
| AI 노동력 장터 | AI 회사가 전문가를 시간제로 씀 | Mercor·Micro1 (미) | Mercor 연매출 환산 $2B·기업가치 협상 $20B (2026-07) / Micro1 총매출 환산 $500M (2026-08) | AI 가 20분 면접으로 전문가를 거르고 일감에 붙임. 사람 검수는 공개 안 함 |
| 사내 인사 문의 해결 | 직원 수천 명 회사 | Leena AI·Ema·ServiceNow·Microsoft Copilot·Lattice·Visier·15Five·Culture Amp (미) | Ema 고객 Wipro 사례 연 290만 건 문의 처리 (2026-09) | Ema 원문 "critical decisions 는 사람 승인". 확신도 낮으면 사람에게 넘김 |
| 제외 — 단순 챗봇·요약 | — | 노동OK 노무 상담 챗봇, 각 사 FAQ 봇 | — | 여러 단계를 스스로 잇지 않아 지도에서 뺌 |

한국·일본·중국·유럽 따로 정리는 4절.

## 2. 제품별 — 실제로 무엇을 스스로 하나

| 제품 | 스스로 하는 것 (기능명 · 출시) | 못 하는 것 · 사람 자리 | 성능 주장 (근거) | 확신도 |
|---|---|---|---|---|
| **Rippling** (미) | Rippling AI (2026-03-18). 회사 인사·급여·기기·지출을 한 데이터로 묶어 물으면 답함 | **급여는 "승인용으로 차려 놓기"까지만** — 원문 "stages the payroll run for your approval" | "정확한 답이지 어림짐작이 아니다"(자체). 자체 설문: 회사 10곳 중 약 8곳(79%)이 작년에 급여 오류를 한 번은 겪음 | FACT(기능·문구) / LIKELY(수치, 자체 설문) |
| **Deel** (미) | AI Workforce 베타 (2025-08-21). 에이전트 7개 — 채용 나라 추천(Hiring Guru), 휴가 공백 표시(Time Off Fairy), 원격근무 세금 위반 감지(Border Buddy), 교대 공백 찾기(Schedule Sheriff), 기기 추천(IT Guy), 퇴직 절차 추천(Goodbye Genie), **급여 이상 사전 감지(Payroll Detective)** | **7개 전부 "추천한다·미리 표시한다" 로만 적혀 있음. 스스로 실행하는 에이전트 0개** | 플랫폼 안에서 "아낀 시간·처리한 일·줄인 오류" 를 잰다고만 하고 숫자는 공개 안 함 | FACT(원문 직접 확인) |
| **Workday** (미) | Agent System of Record (ASOR) — **AI 에이전트 자체를 직원처럼 등록·권한 부여·감시하는 장부** (정식 출시 2026년 상반기). Payroll Agent·Contract Intelligence Agent (2025-09-16). Agent Passport — 에이전트를 출시 전후로 계속 시험 (2026-06-02) | ASOR 은 일을 하는 게 아니라 **에이전트를 관리하는 도구**임. 에이전트가 사람 대신 서명하는 기능은 없음 | Payroll Agent "규정 준수 최대 4배 빠름"(초기 도입 고객 기준, 자체) · Contract Agent "계약 체결 시간 65% 단축"(자체) · 고객 11,000+ · 파트너 에이전트 65+ 연결 | FACT(기능) / LIKELY(수치) |
| **Gusto** (미) | AI 비서 Gus (2024년 말). 2026-01-20 OpenAI ChatGPT 디렉터리에 **급여 앱 최초로 등재** | 사용자가 한도를 정해 주면 그 아래에서는 승인 없이 실행 — 즉 **한도를 사람이 먼저 정해야 함** | 수치 없음 | LIKELY (공식 문서 403 으로 원문 대조 실패, 2차 보도만) |
| **ADP** (미) | ADP Assist 에이전트 + Lyric HCM. AWS Bedrock AgentCore 위에 재구축 (2026-09-08) | 공식 원문 "think, plan, and take action **under human oversight**" — 사람 감독이 조건으로 박혀 있음 | 신규 고객 온보딩 핵심 단계 50% 이상 단축(자체). 고객 110만+·140개국 | FACT(원문 문구) |
| **Paylocity** (미) | Paylocity Ignite AI (2026-07-21). Payroll Analysis Agent — 과거 추세와 비교해 **제출 전에** 이상 급여를 찾아냄 | 제출 전 경고까지. 실행은 사람 | 수치 미확인 | LIKELY (공식 보도자료 본문 회수 실패) |
| **HireVue** (미) | AI Interviewer — **"AI 가 묻고, 캐묻고, 듣는 진짜 양방향 음성 대화"** 를 24시간 진행하고, 회사가 준 채점 기준에 맞춰 **점수를 매기고 이유까지 설명함** | 사람 자리 셋 — ① 질문·기준 세팅 ② **후보자가 AI 녹화·평가·채점에 동의해야 시작** ③ 최종 합격 결정 | 지원→면접관 전달 79% 빨라짐(AdventHealth 파일럿). 화면 표기: 관리자 불합격 판정 30% 감소·적격자 60% 증가·완주율 86%·채용담당자 주당 10시간 절약 (전부 자체) | FACT(기능 원문) / LIKELY(수치) |
| **Eightfold AI** (미) | Talent Agents 2.0 (정식 2026-07-15) + AI Interview Companion (2026-04-08). **초기 면접 라운드를 AI 가 대신 봄** — 원문 "Recruiters and hiring managers are freed from repeating the same early-stage interviews" | **마지막 라운드는 사람이 함** — 원문 "a human-led final round still concluding the process" | 채용 주기 42일 → 1주 미만, 면접까지 걸린 시간 최대 90% 단축 (AI Interviewer 초기 도입사, 자체) | FACT(기능·문구) / LIKELY(수치) |
| **Alex** (미) | 투자 $20M (2025-09-29). **스스로 도는 흐름 20개 이상** — 영상·전화 면접 진행, 이력서 심사, 후속 일정 잡기, **가짜 지원자 탐지**, 구조화 기록 작성, 채용관리 시스템 33종에 자동 반영 | 채용담당자는 "관계 쌓기·현업 팀장 자문" 으로 옮긴다고만 함. 합격 결정은 사람 | 누적 면접 100만+ · 후보자 96% 가 Alex 면접을 선호 (자체/3차 재인용) · 직원 52명 | FACT(투자·기능) / LIKELY(수치) |
| **Paradox (Olivia)** (미) | 문자·대화로 현장직 지원부터 면접 예약까지. **2025-10-01 Workday 가 인수 완료**, "Workday Paradox Candidate Experience Agent" 로 판매 중 | 인수 금액 비공개. 구체적 자율 범위는 인수 보도자료에 없음 | Chipotle 채용 소요 12일→4일, GM 연 $200만 절감 (2차 블로그 재인용, 원문 미확인) | FACT(인수) / 미확인(성능) |
| **Mercor** (미) | AI 가 20분 영상 면접으로 전문가를 평가해 AI 학습용 일감에 붙이는 장터. 전문가 30,000+ · 만들어진 일자리 44만 건 · 평균 시급 $112 · 하루 지급액 $400만+ | AI 평가 방식·사람 검수 여부를 공개 안 함 | 연매출 환산 $2B (4개월 만에 2배), 기업가치 $20B 협상 중 (2026-07-09 TechCrunch) | FACT(규모) / 미확인(평가 방식) |
| **Micro1** (미) | 원래 AI 채용 회사였는데, 고객들이 이 시스템으로 데이터 작업자를 뽑는 걸 보고 그쪽으로 방향을 틀었음 | 같음 | 총매출 환산 8개월 만에 $100M→$500M, 순매출 환산 $150~200M, 마진 80~90% (2026-08 TechCrunch) | FACT |
| **Juicebox · Moonhub · SeekOut** (미) | Juicebox PeopleGPT — 말로 설명하면 후보를 찾아옴, 에이전트는 월 $199 추가. Moonhub — 필요할 때 사람에게 넘김. SeekOut Sam — 기준표 기반 비동기 면접 | Moonhub 원문 "전문 인재 파트너가 한 명 한 명 검증한 뒤 팀에 제시". SeekOut 은 "사람이 승인하도록 추천만 올림" | Moonhub: 제시한 후보의 80% 를 고객이 면접함, 채용 기간 50% 단축 (자체) | LIKELY |
| **Lattice** (미) | Lattice AI Agent 전 고객 무료 개방 (2025-10-02). 반복 인사 문의 응대, **번아웃 위험·이탈 신호·피드백 공백을 집어냄** | 2024-07-09 "AI 직원을 인사 시스템에 정식 등록" 발표 → **사흘 만인 2024-07-12 철회.** 원문 "will not further pursue digital workers in the product" | 수치 없음 | FACT(철회 사건 원문 확인) |
| **Ema** (미) | HR·IT·재무 허브 (2026-09-01). "AI 직원" 이 입사 처리를 급여·계정·기기·메일에 걸쳐 **스스로 단계를 짜고, 실행하고, 자기 결과를 검사함** | 원문 "human oversight for **critical decisions**" · "복지 문의가 사실은 임금 분쟁일 때, 접근 요청이 사람 승인을 필요로 할 때" 를 가려낸다고 함 | Wipro: 흐름 100+ 개, 연 290만 건 문의, 응답 며칠→몇 초, **직원 만족도 20% 상승** | FACT(원문) / LIKELY(고객 수치) |
| **Leena AI** (인도/미) | 사내 IT·HR·재무 1·2차 문의 자동 처리 | 복잡한 건은 사람에게 | 직원 질문 70% 이상 즉시 해결(자체), 1·2차 요청 60% 이상 자동화 가능(자체) | LIKELY (누적 투자 $40.1M, 최신 라운드 2021-09 — 2026년 신규 투자 못 찾음) |
| **Visier Manager Agent** (미) | 2025-09-17. 데이터 가져오기·성과 분석·1:1 안건 작성·회의 잡기 | 원문 "keeps the manager in the loop on **critical decisions**" | 목표 정렬로 성과 16% 향상·26% 개선 (자체 인용 연구) | FACT(기능) / LIKELY(수치) |
| **SmartHR** (일) | AI 아시스턴트 — 24시간 365일 현장·매장 문의 즉답. 등록 기업 80,000+ · 앱 250만 설치 (2026-07) · 해지율 기준 유지율 99% (2026-04) | **"AI 에이전트" 로 부르는 자율 실행 기능은 공식 페이지에서 못 찾음** — AI 는 문의 응대뿐 | 수치는 위 규모뿐 | FACT(규모) / 미확인(에이전트) |
| **freee 人事労務** (일) | freee AI 시프트 관리 — 근태 패턴을 등록하면 AI 가 교대표를 짬. 勤怠モニター(특허) — 이상 근태 실시간 감지. freee サーベイ — 이직 징후 시각화 | 발표일 미기재 | 수치 없음 | LIKELY |
| **Factorial** (스페인) | Factorial One (AI 에이전트) — 채용 공고 자동 작성, 상위 매칭 추천, 이력서 즉시 요약. 기업 16,000+ 이용 | 추천까지. **"EU AI Act 요건 준수" 를 제품 페이지에 명시** | 기업가치·출시일 페이지에 없음 | LIKELY |
| **HiBob** (영/이스라엘) | Bob AI — 업무 자동화·개인화 소통·예측 분석·**편향 탐지** | 발표일·고객 규모 미기재 | 없음 | 미확인 |
| **北森 Beisen** (중) | AI招聘助手(채용 비서)·AI面試官(면접관)·AI陪練(연습 상대)·AI學習助手·AI領導力教練·AI員工助手 등 6종 이상 | 자율 범위 공개 안 함 | 매출·ARR 은 IR 메인에 없음, 홍콩거래소 공시 검색 0건 | 미확인 |
| **Moka** (중) | "새 세대 AI 원생 HR SaaS". 2024년부터 대형 모델을 지능형 면접·해외 채용·대화형 분석에 규모화 적용 | 기능명·발표일·규모 못 찾음 | 없음 | 미확인 |
| **원티드랩** (한) | **채용 에이전트 (2025-10-21)** — 조건 필터를 안 쓰고 말로 설명하면 인재풀에서 후보를 찾아 제안까지 한 번에. AI 이력서 코칭 (2025-11-24). IT 인재 380만 명 풀 | 제안을 보낼지는 사람이 정함 | "AI로 10초 만에" 인재 탐색(자체). 2026년 1분기 매출 89억 원, 전년 동기 대비 12.1% 증가 | FACT(출시일·매출) / LIKELY(성능) |
| **그리팅 (두들린)** (한) | 채용관리(ATS)+인재관계관리(TRM) 묶음. Greeting AX (AI 기능). 기업 10,000+ · 누적 관리 지원자 20억+ (2024 기준) | AI 가 스스로 무엇을 끝내는지는 공개 문구로 확인 안 됨 | 면접 일정 조율을 한 번에 줄임 | LIKELY |
| **자버 (jober.io)** (한) | **자버 AI 에이전트** — 근로계약서·전자계약·설문을 단체 카카오톡으로 보내고 수신 확인까지 처리. 기업 20,000+ 이용 | 계약 내용 판단은 사람 | 수치 없음 | LIKELY |
| **마이다스아이티 inAIR** (한) | AI 역량검사(구 AI 면접) — 2018년 출시. 국내 AI 채용 검사의 사실상 표준 | 합격 결정은 사람 | 2018 대한민국 강소기업대상 인공지능 채용솔루션 부문 대상. **타당도(진짜 성과를 맞히는지) 검증 자료를 못 찾음** | LIKELY(출시) / 미확인(타당도) |
| **시프티 · 플렉스** (한) | 시프티 — 전 세계 기업 300,000+ 이 근태·교대 관리에 씀. 플렉스 — "Relations Driven AX", AI 전환을 평가·데이터 구조 쪽으로 밀고 있음 (2025-11~12 글) | **둘 다 자율 실행 에이전트 기능명·출시일을 공개 페이지에서 못 찾음** | 없음 | 미확인(AI 에이전트) |

## 3. 진짜 실력 — 제3자 증거

| 무엇을 재나 | 결과 | 뜻 | 출처 · 날짜 | 확신도 |
|---|---|---|---|---|
| **AI 이력서 심사 인종·성별 편향** (Wilson & Caliskan, AIES 2024) | 백인 이름이 유리한 경우 **85.1%**, 여성 이름이 유리한 경우 **11.1%**, 흑인 남성은 **최대 100% 의 경우에 불리** | 대형 언어 모델에 이력서를 그냥 맡기면 이름만으로 갈림 | arXiv 2407.20371, 2024-07-29 | FACT |
| **AI 추천이 사람 판단까지 흔듦** (Wilson 외, 2025) | 참가자 528명·시나리오 1,526개. AI 가 특정 인종을 밀면 사람도 **최대 90% 의 경우** 그대로 따라감. 편향 자각 검사를 먼저 시키면 고정관념과 다른 후보를 고르는 비율 13% 증가 | "사람이 최종 결정한다" 는 안전장치가 실제로는 안 먹힘 | arXiv 2509.04404, 2025-09-04 | FACT |
| **뉴욕 편향 감사 의무 이행 실태** (Cornell, Wright 외) | 조사한 고용주 **391곳 중 감사 보고서를 실제 올린 곳은 18곳(약 4.6%)**, 고지문을 올린 곳은 13곳 | 세계 최초의 채용 AI 감사법이 사실상 지켜지지 않음 | arXiv 2406.01399 "Null Compliance", 2024-06-03 | FACT |
| **EEOC v. iTutorGroup** | 채용 소프트웨어를 **여성 55세 이상·남성 60세 이상은 자동 탈락** 시키게 짜 놓아 미국 지원자 200명 이상을 걸러냄. 이 사건이 EEOC 의 "AI·알고리즘 공정성 이니셔티브" 출발점 | 사람이 안 봐도 되게 만든 자동 거름망이 곧바로 위법이 된 첫 실례 | eeoc.gov, 사건번호 1:22-cv-02565 (EDNY), 제소 2022-05-05 | FACT |
| **Mobley v. Workday** | 캘리포니아 북부연방지법 Rita Lin 판사, **2025-05-16 전국 단위 집단소송 예비 인용**, 2025-12-02 통지 계획 승인. Workday 측 스스로 대상이 "수억 명(hundreds of millions)" 이 될 수 있다고 진술. 2026년 현재 진행 중 | **채용 AI 를 쓴 회사가 아니라 만든 회사가 직접 피고**가 된 첫 대형 사건 | clearinghouse.net/case/44074 (직접 열람 403, 인용문만 확보) · 로펌 보도 다수 | LIKELY(1차 명령문 미대조) |
| **AI 채용 현장실험** (Li·Raymond·Bergman "Hiring as Exploration") | 콜센터 채용을 "탐색 문제" 로 바꿔 푸는 알고리즘. *Review of Economic Studies* 93(2):1200 (2026) 게재 | 학계는 이 방향을 인정했지만, 잔존율 수치를 원문에서 확인 못 함 | academic.oup.com | LIKELY(서지만 확인) |
| **급여 오류 실태** | Rippling 자체 설문: 회사 10곳 중 약 8곳(79%)이 지난해 급여 오류를 최소 1건 겪음. 한국: 2024년 **외국인 노동자 임금 체불액만 1,548억 원(전년 대비 43.6% 증가), 피해자 30,684명** | 급여 오류는 드문 사고가 아니라 상시 상태임 — 우리 "급여 오류 0건" 지표가 의미 있는 이유 | rippling.com/blog/ai-in-hr · 매일경제 보도(고용노동부 자료 인용) | LIKELY(둘 다 1차 통계 원문 미대조) |
| **AI 면접 타당도** | **AI 면접 점수가 실제 직무 성과를 맞히는지 검증한 신뢰할 만한 제3자 연구를 찾지 못했음.** 비동기 영상면접 예측 타당도 .19 라는 2차 언급만 있고 원문 열람 실패 | 면접을 AI 가 다 보는데, 그 점수가 맞는지 아무도 공개 검증 안 했음 | — | 미확인 |
| **AI 시대 직원 몰입도** (Gallup) | 미국 직원 몰입도 2026년 상반기 **31%** 로 낮음. 다만 **관리자가 팀의 AI 사용을 적극 지원한다고 답한 직원의 몰입도는 48%, 아닌 경우 30%** (18%p 차이) | AI 도입 자체보다 관리자가 어떻게 쓰느냐가 사람 쪽 지표를 가름 | gallup.com/workplace/712433 | LIKELY(게재일 미확인) |
| **반대 증거 한 바퀴** | ① **Lattice** 가 2024-07-09 "AI 직원 정식 등록" 을 발표했다가 반발로 **사흘 만에 철회** ② EEOC 의 2023년 AI 고용차별 지침이 2025년 행정명령 뒤 **조용히 삭제됨**(시점 특정 실패) ③ Deel 의 "에이전트 7개" 는 전부 추천·경고만 함. **"사실은 사람이 한다" 는 폭로나 회사 청산 사례는 찾아봤지만 없었음** | 이 바닥의 실패는 기술이 들통난 게 아니라 **사회적 반발과 규제** 로 옴 | shrm.org (Lattice) · natlawreview.com (EEOC) · deel.com | FACT(Lattice) / LIKELY(EEOC) |

## 4. 나라별 — 무엇이 막고 무엇이 열렸나

| 나라 | 제품 (자율 정도) | 규제 사실 | 우리에게 뜻 | 확신도 |
|---|---|---|---|---|
| **한국** | 원티드랩 채용 에이전트(2025-10-21, 대화로 후보 찾아 제안), 그리팅(기업 10,000+), 자버 AI 에이전트(기업 20,000+, 근로계약서·전자계약), 마이다스 inAIR(2018), 시프티(전 세계 30만 기업), 플렉스, 사람인 AI매치·AI 모의면접, 인크루트 AI 인성검사 V2, 잡코리아 AI 추천 | **공인노무사법 제27조 ①** "공인노무사가 아닌 자는 제2조제1항제1호·제2호 또는 제4호의 직무를 업으로서 행하여서는 아니 된다"(개정 2020-01-29) — 즉 **① 신고·신청 대행 ② 서류 작성 ④ 노무관리진단은 자격자 전속**. ② 항은 노무사인 것처럼 표시·광고하는 것도 금지. **제28조 벌칙**: 제27조제1항 위반 등은 3년 이하 징역 또는 3천만원 이하 벌금, 제27조제2항 위반 등은 1년 이하 징역 또는 1천만원 이하 벌금.<br>**개인정보보호법 제37조의2**(본조신설 2023-03-14) "정보주체는 완전히 자동화된 시스템(인공지능 기술을 적용한 시스템을 포함한다)으로 … 결정이 자신의 권리 또는 의무에 중대한 영향을 미치는 경우에는 … 거부할 수 있는 권리를 가진다" + 설명 요구권 + 기준 공개 의무.<br>**AI기본법** 제2조 고영향 인공지능 정의에 **"채용, 대출 심사 등 개인의 권리·의무에 중대한 영향을 미치는 판단"** 이 명시로 들어가 있음 | **① 채용은 열려 있고 ② 노무 서류·신고 대행은 막혀 있음.** 그래서 한국 제품이 전부 채용·근태·전자계약 쪽에만 몰려 있고, 노무사 일(진정 대응·산재 신청·취업규칙 신고)을 하는 AI 는 한 곳도 못 찾음. 다만 **채용 AI 는 "거부할 권리·설명할 의무·기준 공개" 세 가지를 이미 법으로 져야 함** | FACT(조문) / LIKELY(제품) |
| **일본** | SmartHR (등록 기업 80,000+, 앱 250만 설치, 유지율 99% — 단 AI 는 문의 응대 비서까지), freee 人事労務 (AI 시프트 관리·근태 이상 감지·이직 징후 시각화) | **社会保険労務士法 제27조(業務の制限)** "社会保険労務士又は社会保険労務士法人でない者は、他人の求めに応じ報酬を得て、第二条第一項第一号から第二号までに掲げる事務を業として行つてはならない"(사회보험노무사가 아닌 자는 남의 부탁을 받아 보수를 받고 제2조1항1~2호 사무를 업으로 해서는 안 된다). **제32조의2 제6호** "一年以下の拘禁刑又は百万円以下の罰金"(1년 이하 구금형 또는 100만엔 이하 벌금) | 한국과 같은 구조로 막혀 있음. **그래서 세계 최대급 노무 SaaS 를 가진 나라인데도 "노무사 일을 하는 AI" 가 안 나옴** — SmartHR 조차 AI 는 문의 응대까지임 | FACT(조문, 정부 법령 API 원문 확인) |
| **미국** | 1~2절 대부분 | **뉴욕시 Local Law 144** — 2023-01-01 발효, 2023-07-05 집행 시작. 공식 FAQ 정의: AEDT 는 ① 기계학습·통계모형·데이터분석·AI 를 쓰고 ② 고용 결정을 돕고 ③ **재량 판단을 상당히 보조하거나 대체하는** 도구. 쓰려면 1년 안에 편향 감사를 받고 그 결과를 공개해야 하며, **사용 10영업일 전에 후보자에게 알려야 함**. **Illinois HB 3773** 2026-01-01 시행(채용·승진·해고 AI 차별 금지, 사용 고지 의무, 우편번호 대리변수 금지). **California FEHA 자동화 의사결정 규정** 2025-10-01 시행. **Colorado AI Act** 는 2026-02-01 → 2026-06-30 → **2027-01-01 로 두 번 연기**되며 의무가 크게 축소됨. **EEOC** 의 2023년 AI 지침은 2025년 행정명령 뒤 삭제됨 | **연방은 후퇴하고 주·시가 앞서는 모양.** 자격 전속 제도는 없어서 "누가 해도 되는" 일이지만, **차별했는지를 나중에 숫자로 검사당함** — 우리 쪽으로 옮기면 "행동 기록 + 집단별 통과율 자기검사" 가 필수 재료임 | FACT(LL144 원문·시행일) / LIKELY(주법) |
| **EU** | Personio(독, 접속 차단으로 미확인), Factorial(스, 기업 16,000+, "EU AI Act 요건 준수" 표기), HiBob(영/이스라엘) | **AI Act 부속서 III 4항** — "(a) 자연인의 **모집 또는 선발**에 사용되는 AI (b) **근로관계 조건, 승진 또는 해지**에 영향을 주는 결정, 업무 배정, 그리고 그 관계 속 사람의 **성과와 행동을 감시·평가**하는 AI" 는 전부 고위험. 원 적용일 2026-08-02 → Digital Omnibus 잠정 합의로 **2027-12-02 로 연기**(2026-05 합의, 관보 게재 전) | **채용뿐 아니라 평가·승진·해고·근태 감시까지 통째로 고위험.** 우리 직종표의 "인사 평가·보상" 도 유럽에서는 고위험 칸에 들어감 | FACT(조문) / LIKELY(연기) |
| **중국** | 北森 Beisen — AI 채용 비서·AI 면접관·AI 연습상대·AI 학습비서·AI 리더십 코치·AI 직원비서 등 6종 이상. Moka — "새 세대 AI 원생 HR SaaS", 2024년부터 지능형 면접·해외 채용에 대형 모델 적용 | 채용 AI 전용 규제는 찾지 못함 | 제품 종류는 가장 많은데 **규모·자율 범위가 전부 비공개**라 실력을 판단할 수 없음 | 미확인 |

## 5. 우리 정의 문서와 대조

### 5-1. "대체의 뜻" 으로 재면

| 우리 기준 | 남들 현황 | 판정 |
|---|---|---|
| 사람이 중간에 확인·고치면 아직 대체 아님 | 급여·노무는 전원 사람 승인(Rippling "승인용으로 차려 놓음", Deel 에이전트 7개 전부 추천만, ADP "사람 감독 아래"). 채용은 **면접·채점까지는 AI 혼자 끝내지만 합격 결정은 전부 사람** | **대체 0건.** 다만 채용 면접은 우리 기준으로 "한 덩어리 일을 끝까지 한" 첫 사례에 가장 가까움 |
| 사람 부르는 다섯 경우 (되돌릴 수 없음·승인 조건·판단 안 섬·한도 초과·자격자 전속) | 급여 지급·세금 신고 = **되돌릴 수 없음**. Gusto 의 사용자 설정 한도 = **한도 초과**. Ema 의 "critical decisions" · Visier 의 "keeps the manager in the loop" = **승인 조건**. 한국 노무 서류·일본 노무 신고 = **자격자 전속**. ServiceNow 계열은 **확신도 점수가 낮으면 사람에게 넘김** | 다섯 경우 중 넷은 이미 업계 관행. **"판단이 안 서서" 를 스스로 알고 부르는 장치는 확신도 점수 방식으로 3차 자료에만 언급될 뿐, 어느 회사도 임계값과 작동 방식을 공개하지 않음** |
| 초보와 전문가를 가르는 5단계 (보기·알기·정하기·하기·끝내기) | **보기**: 급여 이상 감지(Deel Payroll Detective·Paylocity), 이력서·면접 읽기는 이미 사람 위 속도. **알기**: 나라별 노동법 지식은 Deel 이 150개국 현지 전문가 2,000명 지식을 학습했다고 주장. **정하기**: 여기서 갈림 — 추천까지만. **하기**: 면접 진행은 하고, 급여 실행은 못 함. **끝내기**: 아무도 안 함 | **정하기·끝내기가 비어 있음.** 법률과 똑같은 자리에서 끊김 |

### 5-2. 9계통 재료 중 남들이 가진 것

| 계통 | 남들이 이미 가진 것 | 비어 있는 것 |
|---|---|---|
| **환경** | 급여·근태·기기·계정·메일을 한 플랫폼에 묶음(Rippling·Ema). 채용관리 시스템 33종 자동 연동(Alex). SeekOut 은 MCP 로 Claude·ChatGPT 에 붙임. Gusto 는 ChatGPT 디렉터리에 급여 앱 최초 등재(2026-01-20) | **정부 시스템 직접 제출이 없음** — 4대보험 신고, 노동위 구제신청, 산재 요양급여 신청을 AI 가 넣는 제품 0개 |
| **자료·검색** | 150개국 노동법·세법 규칙(Deel), 인재풀 380만(원티드)·3만 전문가(Mercor), 누적 지원자 20억(그리팅) | 판례·노동위 판정례를 붙인 제품 못 찾음 |
| **지식·경험** | 현지 전문가 2,000명 지식 학습 주장(Deel), 채점 기준표(rubric) 기반 면접(HireVue·SeekOut) | **"20년차 노무사가 아는 정석" 을 적어 둔 지식체계 없음.** 특히 산재·부당해고는 제품 자체가 없음 |
| **기억·상태** | 직원 생애주기 데이터 한 곳(Workday·Visier), 후보 관계 관리(TRM, 그리팅) | 사건 단위 장부(진정 1건, 산재 1건)를 끌고 가는 구조 없음 |
| **규칙·권한** | **Workday ASOR** — AI 에이전트를 직원처럼 등록·권한 부여·비용 추적·감사하는 장부(정식 출시 2026). Agent Passport 로 출시 전후 계속 시험. Ema 는 역할 기반 권한 + 전 행동 감사기록 | **임계값 공개 0건.** "이 정도면 내가 못 하겠다" 를 스스로 판정하는 기준을 아무도 안 밝힘 |
| **행동 체계** | 스스로 도는 흐름 20개+(Alex), 에이전트 7종(Deel), 6종+(Beisen), 입사 처리 100+ 흐름(Ema Wipro) | 처음 보는 상황에서 길 찾기 — 전부 정해 둔 흐름 안에서만 돎 |
| **실무** | 면접 진행·채점, 급여 이상 감지, 교대표 짜기, 근로계약서 발송, 입사·퇴사 처리, 문의 응대 | **노무사 일 전체가 비어 있음** — 취업규칙 작성·신고, 노동청 진정 대응, 노동위 구제신청 서면, 산재 신청·불승인 뒤 심사청구. 한·일 둘 다 자격 전속이라 아무도 안 만듦 |
| **검증·평가** | 편향 탐지(HiBob), 가짜 지원자 탐지(Alex), 급여 이상 사전 감지(Deel·Paylocity), 뉴욕 편향 감사(법으로 강제) | **성과 지표로 재는 곳을 한 곳도 못 찾음.** 우리 표의 지표(입사 90일·1년 정착률, 핵심 인재 이직률, 노동위 인용률, 산재 승인율, 과태료 건수, 급여 오류로 더 나간 비용) 대신 전부 "시간·건수·비용 절감". 그나마 결과에 가까운 건 Ema 의 직원 만족도 20% 상승 하나뿐이고 그것도 자체 발표. **AI 면접 점수가 진짜 성과를 맞히는지 검증한 제3자 연구도 못 찾음** |
| **학습·개선** | Deel 이 플랫폼 안에서 "줄인 오류" 를 잰다고 말은 함(숫자 비공개) | 결과를 받아 다음에 반영하는 고리를 공개한 곳 없음 |

### 5-3. 첫 직종 고를 때 참고

| 후보 자리 | 남들 성숙도 | 규제 | 성과 지표 재기 | 판정 |
|---|---|---|---|---|
| **노무사 (산재)** | **제품 0개** | 한국 공인노무사법 27조로 신청 대행·서류 작성이 자격자 전속. 일본도 동일 | 산재 승인율·장해 등급·재심사 인용률 — 나라가 결과를 숫자로 돌려줌 | **가장 비어 있고 가장 잘 재짐.** 다만 자격자 전속이라 "노무사가 쓰는 도구" 형태여야 함 |
| **노무사 (분쟁 대리)** | 제품 0개 | 같음. 노동위 대리는 자격자 전속 | 노동위 인용률(5년 평균 32.6%)·화해 조건·체불 회수액 — 기준선이 이미 공개돼 있음 | 비어 있음. 법률의 원고측 인신사고와 같은 "건 단위 위임형" 구조가 가능 |
| **노무사 (자문·급여)** | 플랫폼은 성숙(Rippling·Deel·SmartHR) 하지만 **판단은 전부 추천까지** | 급여 계산·지급은 자격 문제 없음. 4대보험 신고 대행은 한국에서 전속 | 과태료 건수·급여 오류로 더 나간 비용 — 잴 수 있는데 **아무도 안 잼** | **빈 자리가 정확히 "정하기·하기" 칸.** 남들이 추천에서 멈춘 지점을 실행까지 밀면 바로 차이가 남 |
| **채용** | 가장 성숙 — AI 가 면접까지 혼자 봄 | 미국은 편향 감사·고지, EU 는 고위험, 한국은 고영향 + 거부권·설명 의무 | 입사 90일·1년 정착률로 재는 곳 **0개**. 전부 "채용 소요일" 로만 잼 | 경쟁 가장 치열하고 규제 가장 무거움. **다만 "잔존율로 재는 첫 제품" 이 되는 길은 아직 비어 있음** |
| **인사 (평가·보상)** | 문의 응대·분석은 성숙, 평가 자체는 손 안 댐 | EU 는 승진·평가·감시까지 고위험. 한국은 자동화 결정 거부권 대상 | 핵심 인재 이직률·평가 공정성 점수 — 잴 수 있는데 안 잼 | 규제가 채용만큼 무거운데 성숙도는 낮음. 후순위 |
| **인사 (조직·인재개발)** | 몰입도 분석까지 | 상대적으로 가벼움 | 몰입 점수는 업계가 이미 잼(Gallup 31%) | 성과가 사람 여럿에 걸쳐 흩어져 AI 혼자 끝냈다고 말하기 어려움 |

## 6. 못 확인한 것

- **AI 면접 타당도** — AI 면접 점수가 실제 직무 성과를 맞히는지 검증한 제3자 연구를 못 찾음. 예측 타당도 .19 라는 2차 언급만 있고 원문 열람 실패. 이 바닥에서 가장 큰 구멍임
- **마이다스 inAIR 의 타당도·공정성 검증** — 국내 학술·언론 검증 자료를 못 찾음. 회사 공식 도메인 접속 실패(midashri.com ENOTFOUND)
- **뉴욕 Local Law 144 과태료 액수** — 공식 FAQ 에 액수가 없고, 2차 자료는 하루당 $500~$1,500 라고 하나 조문 원문 대조 실패. 실제 과태료 부과 사례도 못 찾음
- **Mobley v. Workday 1차 명령문** — clearinghouse.net 403. 날짜·판사·규모는 2차 인용으로만 확인
- **EEOC 2023년 AI 지침 삭제 시점** — "조용히 내렸다" 는 서술만 있고 정확한 날짜 못 찾음
- **AI기본법 시행일 판본 충돌** — 법률 조사에서는 2026-01-22 시행, 이번 조사에서는 공포 2026-01-20·시행 2026-07-21 인 판본(MST 282791)이 잡힘. 개정본으로 보이나 확정 못 함. **채용이 고영향에 들어간다는 사실 자체는 조문에서 확인됨**
- **Personio** — 접속 차단(HTTP 429)으로 전면 미확인. **Beisen·Moka 규모** — 홍콩거래소 공시 검색 0건, IR 페이지에 매출 없음
- **플렉스·시프티의 AI 에이전트 기능명·출시일** — 공개 페이지에서 못 찾음. 둘 다 AI 를 말은 하는데 자율 실행 기능을 특정할 수 없음
- **일본 社労士 업무를 하는 AI 서비스** — 이름조차 특정 못 함. 후생노동성 AI 채용 지침도 못 찾음
- **뉴플로이·알밤·페이워크·노동OK 챗봇·클랩(CLAP)** — 1차 자료 접근 실패
- **EY 급여 오류 비용 연구, 한국 임금체불 고용노동부 1차 통계** — 원문 404·차단. 언론 경유 수치만
- 검색 예산: 이 세션 WebSearch 200회 한도가 조사 도중 소진되어, 이후는 WebFetch 로 알려진 URL 을 직접 두드리는 방식으로만 진행함. 위 항목들 상당수가 그 때문에 남음

## 7. 출처 (확인일 2026-09-11)

| 대상 | URL |
|---|---|
| Rippling | rippling.com/blog/introducing-rippling-ai · rippling.com/blog/ai-in-hr · sacra.com/c/rippling |
| Deel | deel.com/blog/deel-launches-ai-workforce · news.crunchbase.com/venture/deel-ai-hr-payroll-unicorn-saas-ribbit-a16z |
| Workday · ASOR · Paradox | workday.com/en-us/artificial-intelligence/agent-system-of-record.html · blog.workday.com/en-us/managing-ai-powered-future-of-work.html · newsroom.workday.com/2025-09-16-Workday-Illuminate-TM-Expands-with-New-AI-Agents · prnewswire.com/news-releases/workday-completes-acquisition-of-paradox-302571738.html |
| Gusto · ADP · Paylocity | support.gusto.com/article/250211164235690 · thenewstack.io/gusto-cofounder-small-business-ai · mediacenter.adp.com/2026-09-08-ADP-Partners-with-AWS · paylocity.com/company/about-us/newsroom/press-releases/paylocity-launches-ignite-ai |
| HireVue | hirevue.com/platform/ai-interviewer · hirevue.com/platform/ai-hiring-agents |
| Eightfold | eightfold.ai/company/press/press-releases/eightfold-ai-expands-talent-agents-across-the-full-interview-journey · eightfold.ai/company/press/press-releases/eightfold-ai-grows-talent-agents-to-2-0 |
| Alex | prnewswire.com/news-releases/alex-secures-20m-to-revolutionize-ai-powered-recruiting-302569001.html |
| Mercor · Micro1 | techcrunch.com/2026/07/09/mercor-is-in-talks-for-a-20b-valuation · mercor.com · techcrunch.com/2026/08/20/ai-data-startup-micro1-reaches-500m-gross-run-rate |
| Moonhub · Juicebox · SeekOut | moonhub.ai · juicebox.ai · seekout.com/blog/agentic-ai-recruiting-leveled-up-with-seekout |
| Lattice (철회 사건 포함) | lattice.com/blog/lattice-ai-agent-is-now-available-to-all-customers · shrm.org/topics-tools/news/technology/lattice-scraps-plans-to-treat-ai-bots-as-employees-after-backlash |
| Ema · Leena AI · Visier · 15Five · Culture Amp | globenewswire.com/news-release/2026/09/01/3354202 · blog.leena.ai/agentic-ai-back-office-operations-2026 · prnewswire.com/news-releases/visier-unveils-manager-agent-302559336.html · finance.yahoo.com/news/hr-leaders-meet-amaya-174500042.html · cultureamp.com/company/announcements/culture-intelligence-in-daily-tools |
| Microsoft Copilot HR | microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/transform-hr-with-ai-powered-agents |
| 일본 SmartHR · freee | smarthr.jp · smarthr.jp/function · freee.co.jp/hr |
| 일본 社労士法 27조·32조의2 | laws.e-gov.go.jp (LawId 343AC1000000089) |
| 중국 Beisen · Moka | ir.beisen.com · mokahr.com |
| 유럽 Factorial · HiBob · Personio | factorialhr.com/ai · hibob.com/ai · personio.com (접속 차단) |
| 한국 원티드랩 | blog.wantedlab.com · wantedlab.com |
| 한국 그리팅·자버·시프티·플렉스·마이다스 | greetinghr.com · jober.io · shiftee.io · flex.team · flex.team/blog · group.midasit.com |
| 한국 법령 (공인노무사법·개인정보보호법·AI기본법) | law.go.kr Open API — 공인노무사법 MST 243059 · 개인정보보호법 MST 283839 · AI기본법 MST 282791 |
| 뉴욕 Local Law 144 | nyc.gov/site/dca/about/automated-employment-decision-tools.page · nyc.gov/assets/dca/downloads/pdf/about/DCWP-AEDT-FAQ.pdf · codelibrary.amlegal.com/codes/newyorkcity/latest/NYCrules/0-0-0-138393 |
| EU AI Act 부속서 III | artificialintelligenceact.eu/annex/3 |
| 미국 주법 (Illinois·Colorado·California) | ilga.gov HB3773 (접속 실패, 로펌 요약 경유) · hunton.com · paulhastings.com |
| EEOC v. iTutorGroup · Mobley v. Workday | eeoc.gov/newsroom/eeoc-sues-itutorgroup-age-discrimination · clearinghouse.net/case/44074 |
| 편향 연구 | arxiv.org/abs/2407.20371 (Wilson & Caliskan, AIES 2024) · arxiv.org/abs/2509.04404 (Wilson 외 2025) · arxiv.org/abs/2406.01399 (Wright 외, Null Compliance) |
| 채용 알고리즘 실험 | academic.oup.com/restud/article-abstract/93/2/1200/8160842 (Hiring as Exploration) |
| 몰입도·임금체불 | gallup.com/workplace/712433 · blog.perceptyx.com/what-23-million-employees-say-about-engagement-in-2026 · jntimes.kr/news/articleView.html?idxno=87344 (고용노동부 자료 인용) |
