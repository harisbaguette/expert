# 바깥 조사 — 법률 AI 에이전트 뜯어보기 (안에서 어떻게 돌아가나)

[바깥조사-법률-AI-에이전트.md](바깥조사-법률-AI-에이전트.md) 가 "누가 뭘 만들었나" 라면, 이 문서는 **그 안이 어떤 순서·부품으로 돌아가나** 를 적은 것임. 우리 전문가 에이전트를 만들 때 베낄 부품과 아무도 못 만든 빈자리를 가르는 재료임.

확인일 2026-09-11. 일꾼 7팀(하위 20여 명)이 회사 블로그·도움말·특허·소장·채용공고·공개 코드를 직접 열어 모은 것을 부모가 대조해 씀. 확신도: **FACT** = 1차 자료(회사 공식 글·특허·법원 서류·코드) 직접 읽음 · **LIKELY** = 2차 자료나 자체 발표만 · **미공개** = 어디에도 없음.

뜯은 대상 19개 중 18개 마침(인텔리콘은 사이트를 못 찾아 못 뜯음). 공개 코드 3개 추가로 열어 봄.

## 1. 한 줄 결론

18개가 안쪽 뼈대는 거의 같음 — **① 여러 회사 모델을 일 종류별로 골라 쓰고 → ② 계획을 먼저 보여 승인받고 → ③ 규칙(플레이북) 한 줄마다 작은 에이전트를 붙여 동시에 돌리고 → ④ 나온 문장을 조각내 근거와 하나씩 맞춰 보고 → ⑤ 변호사가 고치는 걸 지켜봐 다음에 반영함.** 다른 점은 이 다섯 단계 각각에 얼마나 돈과 사람을 넣었나임. 그리고 **"내가 지금 판단이 안 선다" 를 스스로 알아채 사람을 부르는 장치는 18개 중 0개** 가 공개함.

## 2. 공통 뼈대 — 한 건이 들어와 나갈 때까지

| 순서 | 무슨 일 | 대표 구현 (제품) | 확신도 |
|---|---|---|---|
| 1 들어옴 | 문서·사건 데이터가 자리(Word·DMS·CMS·이메일)에서 자동으로 들어옴 | Eve Atlas 는 기록이 도착하는 순간 읽어 CMS 에 다시 써 줌. Harvey·Legora 는 iManage·NetDocuments 를 MCP 로 붙임 | FACT |
| 2 계획 | 할 일을 쪼개 계획을 먼저 보여 주고 범위를 고치게 함 | Harvey Workflow Agents: 계획 미리보기 → 범위 조정 → 승인 → 실행. Legora Agent: 과제 분석 → 도구 선택 → 계획 제안 | FACT |
| 3 나눠 돌림 | 규칙·쟁점 하나마다 하위 에이전트를 붙여 수십 개를 동시에 돌림 | Harvey 플레이북 검토: 규칙 1개 = 하위 에이전트 1개, 각자 문서 사본을 고친 뒤 추적변경으로 합침. Crosby: 계약을 8개로 잘라 8개 에이전트. LBOX: 쟁점별 검색 도구 병렬 호출 | FACT |
| 4 찾아 읽음 | 필요할 때마다 검색 → 읽음 → 충분한지 스스로 판단 → 부족하면 다시 검색 | Harvey 5단계 ReAct(필요 분석 → 출처·질의 선택 → 결과 추론 → 충분성 확인 → 인용 붙여 종합). Lexis 는 조사·웹·고객문서 에이전트 3개를 지휘자가 부름 | FACT |
| 5 확인 | 나온 문장을 주장 단위로 조각내 근거와 맞춤. 판례는 바깥 DB(Shepard's·KeyCite)로 아직 살아 있는지 봄 | Harvey 2단계(주장 분해 → 출처 대조). TR Deep Research 는 "Verify" 를 따로 한 번 더 돎. Eve 는 모든 숫자에 원본 페이지 링크 | FACT |
| 6 넘김 | "검토 준비 상태(review-ready)" 로 사람에게. 서명·제출은 없음 | 18개 전부. Spellbook 은 수락·거부 버튼만, 자동 수락 없음 | FACT |
| 7 배움 | 사람이 고친 것을 다음 제안에 반영 | Spellbook 은 "수락된 문구" 만 1년 보관해 비교. Ironclad 특허는 수락·거부를 허용·차단 목록으로 저장. Crosby 는 변호사 옆에 엔지니어 앉혀 RL 미세조정 | FACT |

## 3. 부품별로 누가 어떻게 했나

### 3-1. 모델 — 한 회사 모델을 안 씀

| 방식 | 누가 | 세부 | 확신도 |
|---|---|---|---|
| 일 종류별로 여러 회사 모델 자동 배분 | Harvey, Lexis, Ironclad, Crosby, EvenUp | Harvey: 추론은 Claude Opus 4.6, 대량 처리는 Sonnet 4.6·Gemini 3 Flash, GPT-5.2 병행. 고르는 잣대는 자체 벤치(BigLaw Bench) + 변호사 선호 시험. Lexis 는 사용자가 Claude Sonnet 4.5·GPT-5.1·o3 중 고르거나 "Best Fit" 자동. EvenUp: Opus 가 설계도 → Sonnet·Haiku 가 세부 작성 | FACT |
| 에이전트 뼈대를 남의 SDK 로 | Harvey(OpenAI Agent SDK), CoCounsel(Claude Agent SDK) | Harvey 는 "에이전트 = 시스템 프롬프트 + 도구 묶음" 만 두고 순서를 코드로 짜는 오케스트레이션을 일부러 안 함 | FACT |
| 자체 모델을 덧학습 | Harvey Tenet, BHSN 앨리비 아스트로, Luminance LPT, EvenUp Piai, LexisNexis(예정) | Harvey Tenet: 오픈 모델 Kimi K3 를 Fireworks 와 약 2개월·B300 150장으로 강화학습(GSPO). 자체 시험(LAB) 전부 통과율 10.8% → 19.7%. 고객 데이터 안 씀. BHSN: 계속 사전학습 + 변호사 피드백 RLHF, 바탕 모델 미공개 | FACT |
| 검색용 임베딩만 자체 | Harvey | voyage-law-2-harvey: 미국 판례 200억 토큰으로 2단계 학습, 엉뚱한 상위 결과 25% 줄고 차원 1/3 | FACT |
| 모델 이름 숨김 | 슈퍼로이어(Claude 3.5 Sonnet 만 공개), LBOX, Supio, Eve(소장에 Anthropic API 명시), Garfield, LegalOn, MNTSQ | — | FACT/미공개 |

### 3-2. 흐름 — 계획 → 승인 → 동시 실행 → 합침

| 제품 | 흐름 | 사람이 끼는 지점 | 확신도 |
|---|---|---|---|
| Harvey 플레이북 검토 | 대장 에이전트가 규칙마다 하위 에이전트 생성(수십 개 동시) → 각자 문서 사본 편집 → 추적변경으로 병합 | 병합 결과를 변호사가 수락·거부 | FACT. 위험 분류 정확도 59→77%, 편집 품질 53→87% |
| Harvey Workflow Agents | 계획 미리보기 → 범위 조정 → 승인 → 에이전트 팀이 병렬 분담 → 검토 준비 산출물. 모든 단계 기록 | 승인 1회 + 마지막 검토 | FACT |
| Legora Agent | 과제 분석 → 도구 선택 → 계획 제안 → 여러 문서·도구에 걸쳐 실행 → 목표 대비 평가 → 미달이면 되돌아가 반복 → 작업창에 산출물 | 계획 승인 + 산출물 승인. "결정 기록(decision log)" 을 사람이 되돌릴 수 있음 | FACT |
| Legora Workflows | 완전 에이전트형 조율층. 노코드 빌더를 일부러 거부 — 사용자는 단계만 정하고 검색 전략은 에이전트가 고름 | 단계 정의 시 역할별 권한 | FACT |
| CoCounsel Brief Builder | "사람이 끼는 에이전트". 관할·당사자·판례 고르는 결정 지점마다 멈춤 | 결정 지점마다 | FACT |
| CoCounsel 계약 도구 | 사실 확인 → 논거 제안 → 인용 붙임 → 마무리 4단계 | 마무리 전 | FACT |
| Lexis Protégé | 지휘자 에이전트가 법률조사·웹검색·고객문서 에이전트 3개를 부름. 조사 에이전트는 질문을 법률 쟁점들로 쪼갬. 2026-08 "Legal Intelligence Engine" 이 모델·에이전트·스킬·콘텐츠를 상황별로 고르고 자기 결과를 다시 고침 | 사람 검토 전 자체 검토 | FACT/LIKELY |
| Ironclad Jurist | Manager(배분·조율) / Review / Drafting / Editing / Research(Bluebook 인용 메모) / Intake(제3자 계약 메타데이터 추출) / Redlining / Conversational Search 8개. "Act Mode" 라는 말은 공식 원문에서 못 찾음 | 위험도 3단계 게이트(저: 이탈 때만 / 중: 발송 전 검토 / 고·신규: 변호사 전권) — 이전 조사에서 LIKELY | FACT(8종)/LIKELY(게이트) |
| Luminance 자율 협상 | 검토 → 위험 조항 수정 → 상대에 개정안 발송 → 응답 추적 → 실시간 대응. 2023 시연은 양쪽 다 Luminance 를 켜고 Word 첨부로 4라운드에 합의 | 사람은 "hard stop(양보 불가)" 만 미리 정함. 라운드 상한·루프 구조 미공개 | MED |
| Crosby | 패러리걸 에이전트가 배분 → 8개 에이전트가 계약 부위 분담 → 신뢰 점수 → 변호사가 약한 곳만 고침 | 낮은 점수 부위 | FACT |
| Garfield | 청구서 올림 → 독촉장(이자 근거 포함) → Companies House 조회 → 소장 → 3갈래(무응답 판결 / 인정 → 합의 / 다툼 → 재판) → 집행 | **모든 단계마다** 의뢰인 승인. "자율 아님" 명시 | FACT |
| Eve | Atlas(기록 도착 즉시 정리) → Agents(사건 상태 바뀌면 자동 발동, 예: 치료 끝나면 청구서 초안 시작) → Auditor(매일 밤 전체 사건 훑어 놓친 것 6종 찾음) → Analyst(읽기 전용 질의) | "허가된 에이전트가 승인된 워크플로 안에서 행동, 사람은 결과 검토" | FACT |
| Eve 소장·특허가 드러낸 코드 수준 | PDF 질의서 → 요청 단위로 쪼갬 → 동시 LLM 호출 → 한 문서로 합침 → 편집기 → 결정론적 .docx 내보내기. 큰 파일은 청크. LLM 출력을 결정론 코드가 해석·검증·역직렬화. Anthropic stop_reason 을 읽어 max_tokens 면 (시스템·사용자·부분 출력) 프롬프트로 이어 씀 | — | FACT(소장 ¶54–99) |
| EvenUp Piai | ① 손글씨·체크박스 문서에서 치료 내역 추출 → ② 여러 병원 기록을 한 연표로 합치며 모순 해소 → ③ 의료·과실·손해 통찰 + 초안. Express(AI 초안 → 로펌 검수) / Expert(AI 초안 → 사내 전문인력 100~150명 재작성 1~5일) | 등급 선택은 상품 티어, 임계값 게이트 아님 | FACT |
| Supio CaseAware | 비정형 자료(기록·청구서·문자·사진·증언) 흡수 → 사실(경찰 보고)과 의견(의사 소견) 구분 → 112개 사건 유형별 렌즈 적용 | 연표는 사람 전문가가 전부 검증 | FACT |
| LBOX AI 3.0 | 쟁점별로 검색 도구를 병렬 호출하는 Agentic RAG. 초기엔 도구를 과하게 불러 고침 | — | FACT |

### 3-3. 자료·검색 — 벡터 검색만으로는 안 됨

| 장치 | 누가 | 세부 | 확신도 |
|---|---|---|---|
| 법률 전용 임베딩 | Harvey | 위 3-1 | FACT |
| 문단마다 메타데이터·최신성·LLM 관련도 판정 | Harvey | 일반 임베딩 대비 최대 30% 개선, 잣대는 "고정 토큰 예산 안 재현율" | FACT |
| 밀집+구절 혼합 색인 → 교차 인코더 재정렬 → 헤드노트 순위 → 토큰 정렬로 답-출처 결속 | Thomson Reuters 특허 WO2025085566A1 | 실제 제품 적용은 LIKELY | FACT(특허) |
| 판례 DB 는 안 만들고 빌림 | Harvey(LexisNexis Protégé·Shepard's 제휴), Legora(Wolters Kluwer·EDGAR·EUR-Lex·Jus Mundi·Manupatra) | Legora 는 Qura(구조화 법률 DB, 27개 관할) 인수해 "RAG 너머" 주장 | FACT/LIKELY |
| 인용 위치를 문장 색인 포인터로 | Harvey | 셀 단위 퍼지 매칭에서 문장 단위 포인터로 바꿈 | FACT |
| 문서 처리 파이프라인 | Harvey | 추출 → 임베딩 → 색인, 타입 있는 중간 형식(UDF), Arrow IPC | FACT |
| 4백만 판례 + 법령·주석 | LBOX | 판결문을 논술형 문제 + 채점표로 바꿔 벤치 | FACT |
| 요건사실 그래프 DB | 로폼 | 요건–효과 구조 판단. 세부 LIKELY | LIKELY |

### 3-4. 지식·경험 — 플레이북이 곧 전문가 지식

| 제품 | 플레이북 한 줄의 모양 | 만드는 길 | 확신도 |
|---|---|---|---|
| Harvey Playbook Builder | 규칙 = 선호 입장 + 대안 조항 + 에스컬레이션 조건, 각각 출처 인용 | 기존 플레이북·수정 이력 계약·템플릿을 넣으면 질문을 되물으며 초안 | FACT |
| Spellbook | 규칙 = 기본 입장(Primary) + 대안(Fallback) + 위험도(Low/Med/High) + 메모·선호 문구·승인 요청. 결과는 통과(초록)/실패(빨간 점선), 근거 위치로 점프 | 템플릿 복제 / 모범 문서 업로드 / 설명 입력 AI 생성 / 수동 | FACT |
| Legora | 출발 입장 + 레드라인(양보 불가선). Word 안에서 자동 실행 | Portal 로 의뢰인에게도 노출 | FACT |
| CoCounsel | 올린 플레이북을 읽어 선호 조항·협상 가이드·에스컬레이션·대안으로 구조화 | 업로드 | FACT |
| Anthropic 공개 플러그인 | 이탈을 GREEN/YELLOW/RED 로. RED = "허용 범위 밖 또는 정해진 에스컬레이션 조건 → 상급 변호사·외부 변호사·사업 결정자 서명 필요" | 플레이북 없으면 "같이 만들지 / 일반 상업 표준으로 갈지" 사용자에게 물음 | FACT(코드) |
| MNTSQ | 대형 로펌(長島·大野·常松) 감수 플레이북 기본 탑재, 유사 과거 안건 자동 검색 | — | FACT |
| Crosby | 변호사가 직접 프롬프트를 씀("context engineering"), 익명화 검토 수천 건 + 손으로 붙인 조항 5만 건 | 의뢰인별 Custom Memory | FACT |
| Luminance | 자사 기서명 계약을 지식 창고 삼아 협상 가능/불가 조건 학습 | — | MED |

### 3-5. 기억·상태 — 사건 단위 창고 + 벽

| 장치 | 누가 | 세부 | 확신도 |
|---|---|---|---|
| 사건 단위 창고 | Harvey Vault(프로젝트 1개 = 사건 1개, 문서 1만 개, 상태 uploaded→processing→ready_to_query), Lexis Vault(1만 개·500MB), CoCounsel Workspaces, Lexis Workrooms | — | FACT |
| 자원 단위 권한 + 이해충돌 벽 | Harvey Spaces(양쪽 관리자 승인, Intapp Walls, 모든 접근 기록), Legora(Zanzibar 방식 권한 시스템, NetDocuments 권한 그대로 상속) | — | FACT |
| 사용자·의뢰인·사건별 "기억" | Harvey(개발 중, 난제가 권한·벽), Crosby Custom Memory, Spellbook(수락 문구 1년) | — | FACT |
| 기관 기억 | Luminance("누가 왜 합의했나" 질의), Eve Atlas(기록을 CMS 에 다시 써서 상태 유지) | — | FACT |

### 3-6. 규칙·권한·게이트 — 사람 부르는 자리

| 게이트 종류 | 누가 | 확신도 |
|---|---|---|
| 결정 지점마다 멈춤 | CoCounsel Brief Builder, Garfield(모든 단계), Anthropic 플러그인(입장·기한·초점 질문) | FACT |
| 계획 승인 1회 | Harvey Workflow Agents, Legora Agent | FACT |
| 위험도 등급별 | Ironclad 3단계(LIKELY), Anthropic 플러그인 GREEN/YELLOW/RED + 5×5 위험 행렬(FACT) | — |
| 신뢰 점수 낮은 곳만 | Crosby, CoCounsel(저신뢰 지점 자체 표시) | FACT/LIKELY |
| 바깥 공유·권한 변경은 관리자 승인 + 감사 기록 | Harvey(승인·거부·권한 변경 시각 기록, 1~10년 보관), Legora(보안 로그 12개월+), Google Gemini Enterprise(Cloud Audit Logs 4종) | FACT |
| 도구 자체를 못 쓰게 막음 | Claude Agent SDK(하위 에이전트 tools 목록 밖 도구는 세션에 없음, PreToolUse 훅이 호출 직전에 deny, 권한 모드 6종) | FACT(문서) |
| 자격자 전속 회피 | Eve Jenny(법률 자문 안 함·이름·전화 확인·사람에게 따뜻하게 넘김), Garfield(인가 변호사가 책임) | FACT |
| **숫자 임계값(금액·이탈 정도)** | **18개 중 0개 공개** | 미공개 |
| **"판단이 안 선다" 자각** | **18개 중 0개 공개** | 미공개 |

### 3-7. 검증·평가 — 어떻게 틀렸는지 알아내나

| 장치 | 누가 | 세부 | 확신도 |
|---|---|---|---|
| 주장 분해 → 출처 대조 | Harvey | 환각 = "출처가 반박하는 주장". Harvey 0.2% vs Claude 0.7% / ChatGPT 1.3% / Gemini 1.9%(자체 벤치) | FACT(방법)/LIKELY(수치) |
| 구절 단위 링크 강제 | Harvey Source Score, Eve(모든 숫자 → 원본 페이지), Supio(인용 정밀도 97%+ 자체) | — | FACT |
| 판례 생사 확인 | Lexis Shepard's(A 가 B 인용, 뒤에 같은 관할 C 가 A 를 안 언급하고 B 를 뒤집으면 경고 = At Risk. 부정 표시 5종), TR KeyCite | 연결 안 되는 인용은 수동 확인 표시 | FACT |
| 별도 재검증 패스 | TR Deep Research Verify, Lexis Engine 자체 재검토, Eve Auditor(매일 밤) | — | FACT |
| 변호사 채점표 + LLM 심판 | Harvey BigLaw Bench(점수 = (긍정−감점)/긍정 총점, LAB 은 원자 단위 통과/실패), Legora BAR(체크리스트 상·중·하 가중, 3회 실행, LLM-as-a-judge, 인용 점수·근거 점수 따로), LBOX(판결문 → 논술 채점표, 추론 과정도 채점) | — | FACT |
| 운영 감시 | Harvey(야간 카나리, 버전 붙인 평가 데이터, leave-one-out 게이트), CoCounsel CoCoBench(자동층: 일관성·회귀·인용 근거 + 변호사층: 정확·완결·가독) | — | FACT |
| 결정론 코드로 LLM 출력 검증 | Eve(소장), Anthropic 플러그인 | 출력 형식·역직렬화를 코드가 잡음 | FACT |
| 사람 100명+ 전수 검수 | EvenUp(매주 수천 건), Supio(연표 전부) | Business Insider 2024-12: AI 오류(부상 누락·허위 진단)를 사람이 새벽까지 걸러냈다는 전직원 증언 | FACT/LIKELY(2차) |
| 바깥 평가 | Stanford arXiv:2405.20362 — Lexis+ AI 65% 정답·17% 환각, Westlaw AI-AR 33% 환각. CoCounsel 은 시험 안 됨 | — | FACT |

### 3-8. 학습·개선 — 고친 것이 어디로 가나

| 고리 | 누가 | 세부 | 확신도 |
|---|---|---|---|
| 변호사 A/B·선호 시험이 출시를 결정 | Harvey(Likert 1~7, GPT-4.1 전환 결정), LBOX(ALR 팀 법리 판단) | 모델 재학습이 아니라 **선택** | FACT |
| 수락된 문구만 저장해 다음 제안과 비교 | Spellbook Preference Learning | 편집 내용 아님, 고객 간 공유 없음, 1년 만료 | FACT |
| 수락·거부를 허용·차단 목록으로 | Ironclad 특허 US11960849B2 | 어떤 조항을 분석할지 조정. 모델 재학습 아님 | FACT |
| 변호사 옆 엔지니어 + RL 미세조정 | Crosby | 코멘트 생성에 RL, 의뢰인별 미세조정·평가, "살아 있는 데이터셋" | FACT |
| 사람 검수 → 모델 개선 명시 | EvenUp Piai, BHSN(RLHF) | — | FACT |
| 현장 엔지니어(FDE)가 주 단위로 고침 | Legora, Harvey | 채용공고에 Legora 는 ML 엔지니어·미세조정 직무 없음 | FACT |
| **사용자 편집이 모델 학습으로 간다는 증거** | **18개 중 0개** | 다 "고객 데이터로 학습 안 함" | FACT |

## 4. 제품별 10칸 표 (자세히 나온 것만)

칸: ① 모델 ② 자리 ③ 흐름 ④ 검색 ⑤ 지식 ⑥ 기억 ⑦ 게이트 ⑧ 검증 ⑨ 학습 ⑩ 근거 종류. 3절에 다 나온 칸은 "3-n 참조" 로 줄임.

### Harvey (미)
| 칸 | 내용 |
|---|---|
| ① | 멀티모델(Opus 4.6·GPT-5.2·Sonnet 4.6·Gemini 3 Flash), 자체 덧학습 Tenet, 자체 임베딩. 초기 OpenAI 맞춤 판례 모델(LIKELY) |
| ② | Word·Outlook 애드인, M365 Copilot, iManage·NetDocuments·SharePoint·Drive·Aderant, Email Harvey, API+MCP 커넥터(2026-06 조기 접근) |
| ③ | OpenAI Agent SDK 도구 호출 루프. 3-2 두 줄. Workflow Builder 는 말 또는 노코드 블록(입력·선례·분기) |
| ④ | 3-3. 판례는 LexisNexis 제휴 |
| ⑤ | Playbook Builder, Vault 지식 창고. PwC 세무 맞춤 모델(전문가 피드백, 선호 91%) |
| ⑥ | Vault·Spaces·Memory(개발 중). AES-256·BYOK |
| ⑦ | 승인·거부·권한 변경 감사 기록, 바깥 공유는 관리자 승인, 그룹 자동 권한. 법률 업무 위험 등급은 미공개 |
| ⑧ | 3-7. 인용 자동 검증 95%+(변호사 검증 벤치) |
| ⑨ | 전문가 선호 시험이 출시 결정. 채용공고: 하루 수백만 요청을 배분하는 모델 프록시, Python/Go/TS/K8s/Azure/GCP |
| ⑩ | 회사 블로그 20여 편(FACT), 개발자 문서, 채용 API, 언론 1건 |

### Legora (스웨덴)
| 칸 | 내용 |
|---|---|
| ① | Claude Sonnet 4(내부 평가 +18%), Azure OpenAI GPT-4o·o1 병행. 자체 미세조정 모델 없음 |
| ② | iManage API, NetDocuments MCP + Legal Context Graph(권한 상속·이해충돌 벽), Word·Outlook 애드인 |
| ③ | 3-2. CTO: 하위 에이전트 생성, 파일 읽고 쓰기, 결정 기록, "계약서 자체가 작업창" |
| ④ | 여러 각도 병렬 조사, 1차 출처 대조, 권위 순 정렬, 관할 인식. 청킹·재정렬 세부 미공개 |
| ⑤ | 플레이북(출발 입장·레드라인), 문서 유형별 Workflows, Portal |
| ⑥ | Zanzibar 권한, 논리 테넌트 분리, ISO 27001·42001, 로그 12개월+ |
| ⑦ | Workflows 안 역할별 권한. 위험 등급 미공개 |
| ⑧ | BAR 벤치, 모든 출력이 데이터·프롬프트까지 추적 가능. 자기 검증 에이전트 이름 없음 |
| ⑨ | FDE 주 단위. ML 직무 없음(Node/React/Azure/AWS/GCP/K8s) |
| ⑩ | 회사 사이트·보안 문서·BAR 페이지(FACT), Anthropic·Microsoft 고객 사례(FACT), 팟캐스트 요약(LIKELY) |

### CoCounsel — Thomson Reuters (미)
| 칸 | 내용 |
|---|---|
| ① | 2023 GPT-4 → 2026-08 Claude Agent SDK 로 재구축 + 자체 법률 LLM "Thomson"(표 분석) |
| ② | Word·Outlook·Teams, CoCounsel Legal MCP(Claude 앱에서 호출), iManage·NetDocuments·SharePoint·Box·Litify·Smokeball·HighQ·DeepJudge·Reveal |
| ③ | 3-2 두 줄 + Deep Research Verify |
| ④ | Westlaw Deep Research + KeyCite + Practical Law. 특허 WO2025085566A1 |
| ⑤ | 플레이북 업로드 구조화, Knowledge Search 가 고객 파일과 Westlaw 를 한 층에서 |
| ⑥ | Workspaces(세션·동료·사건 넘어 유지), Syncly. 고객 데이터 학습 안 함 |
| ⑦ | SOC2·ISO42001, 사람 입력 대기, 클릭 가능한 각주. 역할표 미공개 |
| ⑧ | 2023 Trust Team 약 4,000시간(질문 3만+), 출시 전 변호사 400명 5만 회. CoCoBench. 50개 복잡 과제 6시간→8분, 전문가보다 40% 나음(자체) |
| ⑨ | "Behind the Build" 베타 피드백 군집화, 저신뢰 지점 자체 표시 |
| ⑩ | 보도자료·제품 페이지·블로그(FACT), 특허(FACT), Stanford 논문(FACT) |

### Lexis+ AI / Protégé — LexisNexis
| 칸 | 내용 |
|---|---|
| ① | 여러 LLM 혼합, 사용자 선택 또는 Best Fit. 맞춤 모델 2026 말 예정 |
| ② | M365 전 제품, Copilot 맞춤 에이전트, iManage·SharePoint·OpenText·Drive·NetDocuments, API. MCP 언급 없음 |
| ③ | 3-2 |
| ④ | 2,000억+ 문서, AI 헤드노트, 모든 인용에 Shepard's 신호 |
| ⑤ | Practical Guidance(변호사 2,000명·25분야)를 1차 법원과 같은 층에서 |
| ⑥ | Vault(1만 개·500MB), Workrooms |
| ⑦ | Workrooms 이중 승인·최소 권한·RBAC·감사(LIKELY). "사람 검토 전 자체 검토" |
| ⑧ | Shepard's At Risk, 프롬프트마다 5단계 RAG 점검(의미 이해·최신성 필터·권위 순위·인용 검증), Stanford 65%/17%, 자체 비교 Shepard's 98.7% vs KeyCite 77.3% |
| ⑨ | 주 1,000건+ 고객 인터뷰, 멀티모델 + 전문가 미세조정 + 증류 |
| ⑩ | 회사 보도·제품 페이지(FACT), RELX 발표(FACT), Stanford(FACT), 자체 비교(LIKELY) |

### 계약 3사 — Luminance(영) · Ironclad(미) · Spellbook(캐)
| 칸 | Luminance | Ironclad | Spellbook |
|---|---|---|---|
| ① | 자체 LPT(1.5억 문서). 3자 분석은 MoE + 외부 모델 혼합(MED) | Claude·ChatGPT 를 MCP 로 연동, 내부 모델 미공개 | 미공개 |
| ② | Word·Email Agent·Salesforce·DocuSign·SharePoint | Word·Slack·Teams·DocuSign·Salesforce·Drive, REST API | Word 애드인(세부 미공개) |
| ③ | 3-2 | 3-2 8종 | Associate 는 올린 문서 전부 훑어 한 번에 답. 단계·오케스트레이터 미공개 |
| ④ | Lumi 질의응답(출처 표시), 전사 계약 필터·비교 | 미공개 | 조항 라이브러리 폴더 검색, 언어 맞춰 삽입 |
| ⑤ | 기서명 계약 = 지식 창고 | 특허: 조항 유형 약 200개 라이브러리(도움말 차단) | 3-4 |
| ⑥ | 기관 기억 | 특허 US12541643B1: 충돌 편집 3-way 병합 | 검토 조각 1년 보관 |
| ⑦ | hard stop 만 사람, RBAC·MFA·전 접근 추적. 임계값 미공개 | 3단계 게이트(LIKELY), 불변 감사 기록 | 역할 4단계(Admin/Editor/Viewer/Consumer), 승인 대기열 없음 |
| ⑧ | 미공개 | 미공개 | 추적변경 토글, 수락·거부만. 자체 검증 없음 |
| ⑨ | 미공개 | 특허 US11960849B2 허용·차단 목록 | Preference Learning |
| ⑩ | 보도·제품 페이지·시연 기사 | 보도자료·특허. 도움말 403 | 도움말 센터 다수·약관(FACT). 특허 없음 |

### 소송 3사 — EvenUp · Eve · Supio (미, 원고측 인신사고)
| 칸 | EvenUp | Eve | Supio |
|---|---|---|---|
| ① | Claude(Opus 설계 → Sonnet·Haiku 작성) + OpenAI, 자체 Piai | 소장에 Anthropic Claude API. 이름 미공개 | 미공개(제3자 모델, 재학습 금지) |
| ② | Litify 원클릭, SmartAdvocate·CASEpeer, SharePoint·Drive·Dropbox | SmartAdvocate·Litify·Prevail, Clio Grow·Lead Docket, Jenny 음성 24시간 | 문서 업로드 |
| ③ | 3-2 | 3-2 두 줄 | 3-2 |
| ④ | 해결 사건 20만+, 합의 저장소(부상·치료·보험 한도로 검색) | 검증된 판례 DB 만("Legal Research Isolation") | — |
| ⑤ | 승소 청구서 경험으로 미세조정 | Auditor 6종(미진단 TBI·처방됐으나 안 한 MRI·집단소송 자격·영구 장애·SSD·보장) | 사건 유형 112개 렌즈 |
| ⑥ | 미공개 | Atlas 가 CMS 에 다시 씀 | HIPAA 폐쇄 시스템 |
| ⑦ | Express/Expert 는 상품 티어. 변경은 독립 1인 이상 승인 | 허가된 에이전트 + 승인된 워크플로. Jenny 발동 조건 미공개 | — |
| ⑧ | 정확도: 의료비 95%(GPT-4 80%)·치료 91%·날짜-제공자 90%. 사람 100~150명 매주 수천 건 | 모든 숫자 → 원본 페이지 링크, 놓친 청구서 표시, 자체 검증 프레임워크. % 없음 | 인용 정밀도 97%+, 사람 전수 |
| ⑨ | 사람 검수 → 모델 개선 명시 | 미공개 | 미공개 |
| ⑩ | 자사 블로그·Anthropic 사례·채용(벡터 DB·RAG·LoRA)·BI 2차 | 자사 글·소장 US 12,461,932 원문 37쪽 | 자사 글 |

### AI 로펌·일본·한국 — 자세히 못 뜯은 것은 한 줄
| 제품 | 나온 것 | 안 나온 것 |
|---|---|---|
| Crosby(미, PLLC) | 3-1·3-2·3-4·3-8. 4요소 전문 변호사/에이전트/시장 데이터/맞춤 기억. 가드레일 목표 99~99.99%. 협상 시뮬레이션(양측 선호를 각자 에이전트에, 감사 로그)은 연구 단계 | 자체 벤치 점수(신뢰 못 해 폐기) |
| Garfield(영) | 3-2. Xero·Sage·QuickBooks 연동. 인가 변호사 책임 | 모델·지식 형식·기억·정확도·학습 전부 |
| LegalOn(일) | Triage 자동 승인·에스컬레이션 에이전트 존재 | 바탕 모델·임계값 |
| MNTSQ(일) | 3-4 | 10칸 중 6칸 |
| 슈퍼로이어(한) | Claude 3.5 Sonnet(40%+ 빠름), 요청마다 function calling 으로 자료 주문, 인용 적절성 평가로 환각 억제 | 나머지(사이트가 JS 라 못 읽음) |
| LBOX AI 3.0(한) | 3-2·3-3·3-7. 피드백 채널 + NPS → 검증 후 배포 | 모델 이름 |
| BHSN 앨리비(한) | 3-1. EPC 100쪽 1분, ISO27001/27017, Legal OCR 특허 10-2631704, 법률 대화 120만 건 | 바탕 모델. "99.99%" 는 자체 |
| 로폼(한) | Legal Logic Core, 요건사실 그래프 DB, 데이터 500만+ | 세부 |
| 인텔리콘(한) | 못 뜯음 — 사이트 미확인 | 전부 |

### 공개 코드 3개 — 직접 읽은 것
| 대상 | 뼈대 | 우리가 배울 점 |
|---|---|---|
| Anthropic `knowledge-work-plugins/legal` (v1.3.0) | 스킬 9개(review-contract·triage-nda·compliance-check·legal-risk-assessment 등), 각 SKILL.md 가 단계 지시문. MCP: Slack·Box·Egnyte·Atlassian·DocuSign | 실행 전 "어느 편·기한·초점" 질문 → 계약 전체 먼저 읽고 조항 상호작용 본 뒤 GREEN/YELLOW/RED → 전 산출물에 "변호사 검토 필수". 법률 사실 인용 검증은 없음(사내 플레이북 대조만) |
| CourtListener MCP(공식 없음, 커뮤니티 2개) | `courtlistener_verify_citation` 도구가 인용을 파싱해 실제 DB 에 조회 | "상대 변호사 인용이 맞는지 확인" 용도로 명시 — 인용 검증을 도구 하나로 분리한 예 |
| Claude Agent SDK 문서 | 하위 에이전트 = description/prompt/tools/model/permissionMode. tools 밖 도구는 세션에 없음. 권한 모드 6종(default/dontAsk/acceptEdits/bypassPermissions/plan/auto). PreToolUse 훅이 허용·거부 규칙보다 먼저 돌아 deny 가능 | CoCounsel 이 이 위에 재구축됨. "행동하는 자리에서 문을 잠그는 구조" 가 표준 부품으로 있음 |

Google "Gemini Enterprise for Legal" 은 법무 전용 페이지가 없음(4개 URL 전부 soft-404). 범용 플랫폼 + Cloud Audit Logs 만 확인.

## 5. 우리 정의와 대조 — 어디서 베끼고 어디가 비었나

### 9 재료 계통
| 계통 | 베낄 부품 (누구 것) | 아무도 안 한 것 |
|---|---|---|
| 환경 | MCP 커넥터로 DMS·CMS 붙임(Harvey·Legora·CoCounsel). 기록 도착 즉시 발동(Eve Atlas) | — |
| 자료·검색 | 법률 임베딩 + 문단 메타데이터 + LLM 관련도(Harvey). 판례 DB 는 빌림. 문장 포인터 인용 | — |
| 지식·경험 | 규칙 = 선호 입장 + 대안 + 에스컬레이션 + 출처(Harvey·Spellbook). 로펌 감수 플레이북(MNTSQ) | "정석·모르는 것" 을 명시한 20년차 지식체계. 플레이북은 다 계약 조항용 |
| 기억·상태 | 사건 단위 창고 + 자원 권한 + 이해충돌 벽(Harvey Spaces·Legora Zanzibar) | 사건 넘어 배우는 기억은 Harvey 도 개발 중 |
| 규칙·권한 | 결정 지점 멈춤(Brief Builder), 계획 승인(Harvey), 도구 자체 차단(Agent SDK), 감사 기록 | 숫자 임계값, "판단 안 섬" 자각 |
| 행동 체계 | 계획 → 승인 → 규칙별 하위 에이전트 → 병합(Harvey), 목표 미달이면 되돌아감(Legora) | 처음 보는 상황 길 찾기(LAB 전부 통과 19.7%) |
| 실무 | 결정론 코드가 LLM 출력을 잡음, stop_reason 이어 쓰기(Eve 소장), .docx 결정론 내보내기 | — |
| 검증·평가 | 주장 분해 → 출처 대조, 판례 생사 확인, 변호사 채점표 + LLM 심판 3회, 야간 카나리 | 스스로 "이건 못 믿겠다" 고 점수 매기는 건 Crosby 신뢰 점수만 |
| 학습·개선 | 수락 문구 비교(Spellbook), 허용·차단 목록(Ironclad), 선호 시험이 출시 결정(Harvey) | 사용자 편집 → 모델 학습은 0개. 다 "선택" 이나 "목록" 임 |

### 다섯 경우
| 경우 | 업계에 있나 | 어떻게 |
|---|---|---|
| 되돌릴 수 없는 행동 | 있음 | 서명·제출·발송은 18개 전부 사람. Luminance 만 발송을 AI 가 하되 hard stop 안에서 |
| 승인 조건 | 있음 | 결정 지점 멈춤·계획 승인·관리자 승인 |
| 판단이 서지 않는 것 | **없음** | Crosby 신뢰 점수·CoCounsel 저신뢰 표시가 가장 가까움. 자각해서 부르는 장치는 0개 |
| 한도 초과 | 반쯤 | Ironclad 3단계·플러그인 RED 가 "등급" 은 있는데 숫자 임계값은 0개 공개 |
| 자격자 전속 | 있음 | Jenny 자문 회피, Garfield 인가 변호사, 일본 변호사법 72조 선 |

## 6. 못 찾은 것 (재조사 후보)
- 위험도 게이트의 **숫자 임계값** — 18개 전부.
- "판단 안 섬" 을 스스로 알아채는 장치 — 18개 전부.
- Ironclad "Act Mode" 원문·Jurist 조율 방식·도움말 본문(403), Luminance 검증·학습·라운드 상한, Spellbook 바탕 모델.
- Harvey Workflow Builder 노드 이름(User Input/AI Action/Logic/Output 은 3자 주장, 미검증).
- Eve Jenny 사람 넘김 발동 조건, EvenUp 사람 검수 발동 조건, Supio 모델.
- 인텔리콘 전부. Garfield 모델·정확도.
- Business Insider 2024-12 원문(페이월).

## 7. 출처
| 제품 | 1차 출처 (확인일 2026-09-11) |
|---|---|
| Harvey | harvey.ai/blog/why-harvey-is-multi-model-by-design · …/post-training-update-harvey-tenet · …/principles-that-helped-us-scale-agent-development · …/rebuilding-playbook-review-as-a-multi-agent-system · …/how-agentic-search-unlocks-legal-research-intelligence · …/harvey-partners-with-voyage · …/biglaw-bench-retrieval · …/biglaw-bench-hallucinations · …/introducing-biglaw-bench · …/scaling-ai-evaluation-through-expertise · …/playbook-builder-in-harvey · …/harveys-governance-controls · …/connector-library · harvey.ai/platform/workflow-agents · harvey.ai/platform/spaces · developers.harvey.ai/guides/vault · api.ashbyhq.com/posting-api/job-board/harvey |
| Legora | legora.com/product/agent · …/product/workflows · …/product/legal-research · …/landing/playbooks · legora.com/bar · legora.com/security · legora.com/legal/security-measures · claude.com/customers/legora · microsoft.com 고객 사례 · api.ashbyhq.com/posting-api/job-board/legora |
| CoCounsel | thomsonreuters.com 보도 2026-08 · legal.thomsonreuters.com/en/products/cocounsel-legal · legal.thomsonreuters.com/blog/the-next-generation-of-cocounsel-legal · 특허 WO2025085566A1 · arXiv:2405.20362 |
| Lexis | lexisnexis.com 보도(Protégé 2025-12·Engine 2026-08) · RELX 발표 · arXiv:2405.20362 |
| Luminance | luminance.com/autonomous-negotiation · luminance.com/press · luminance.com/security · legaldive.com 시연 기사 · research.contrary.com |
| Ironclad | prnewswire.com 보도 2건 · ironcladapp.com/product/integrations · 특허 US11960849B2 · US12541643B1 |
| Spellbook | help.spellbook.legal(플레이북·Summarize Redlines·Preference Learning·접근 권한) · spellbook.com/legal/terms-of-service |
| EvenUp | evenuplaw.com/piai · …/blog/leveraging-ai-human-review-in-demand-letters · …/blog/claude-for-personal-injury-firms · claude.com/customers/evenup · trust.evenuplaw.com |
| Eve | eve.legal/tort-report/eveos-is-live · eve.legal/platform · eve.legal/trust · lawnext.com 2025-10 · 소장 www.ai.law Corp. v. Butler Labs, Inc. 3:26-cv-05930 (N.D. Cal.) · 특허 US 12,461,932 · EvenUp, Inc. v. Butler Labs, Inc. 4:25-cv-08199 |
| Supio | supio.com/products/medical-chronologies · supio.com/case-aware-ai |
| Crosby·Garfield | sequoiacap.com/podcast/training-data-crosby · crosby.ai · garfield.law · artificiallawyer.com 2025-05-12 |
| 일본·한국 | legalon 공식 · mntsq 공식 · claude.com/customers/law-and-company · blog.lbox.kr/airesearcher · /aisquad · /teamalr · bhsn.ai/newsroom 2025-07-10 · lawform.io |
| 공개 코드 | github.com/anthropics/knowledge-work-plugins (legal/) · github.com/DefendTheDisabled/courtlistener-mcp · github.com/blakeox/courtlistener-mcp · docs.anthropic.com/en/agent-sdk (subagents·permissions·hooks) · cloud.google.com/gemini-enterprise/docs/audit-logging |
