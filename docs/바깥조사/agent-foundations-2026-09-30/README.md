**상업용 자체 개발의 기반 선택은 [상용 개발 후보 목록](상용개발-후보목록.md)을 먼저 본다.** 실행 SDK와 완성형 제품을 포함한 27개 후보의 재사용 범위·라이선스·추가 개발을 정리했다. Python 기반 자체 제품에는 Pydantic AI와 Strands를 우선 비교하고, DeerFlow는 완성형 웹 제품을 개조하거나 기능별 코드를 가져오는 후보로 둔다.

아래는 DeerFlow를 중심으로 완성형 제품의 재사용 범위를 살펴본 자료다. 웹 화면, 실행 환경, 기억, 도구 연결을 가져오고, 직종별 지식·판단·완료 기준과 평가를 추가하는 경우에 해당한다. 경험 축적의 비교 대상으로는 Hermes Agent, 데스크톱 업무의 비교 대상으로는 Agent Zero가 있다.

아래 평가는 문서와 일부 코드 구조에 근거한 도입 우선순위다. 실제 업무 성공률·운영 비용·필요 인력은 아직 비교하지 않았다. 기능 설명은 조사 시점의 기본 브랜치 기준이며, 표시한 릴리스에 모든 기능이 포함된다는 뜻은 아니다. 날짜는 한국 시간이다.

| 후보 | 최신 확인 릴리스 | 가져올 수 있는 부분 | 우리 목적에서의 위치 |
|---|---|---|---|
| [DeerFlow](https://github.com/bytedance/deer-flow) | [v2.1.0 · 9월 24일](https://github.com/bytedance/deer-flow/releases/tag/v2.1.0) | 웹 UI, 프로젝트, 전문 에이전트 설정, 실행 격리, 장기 기억, 도구·스킬, 예약 작업 | **완성형 웹 제품 개조 후보.** 업무 제품의 공통 부분을 넓게 재사용 |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | [v2026.9.24 · 9월 24일](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.24) | 경험에서 스킬 생성·수정, 과거 세션 검색, 기억, 예약 실행, 메신저 | **경험 축적 비교 후보.** 혼자 또는 내부 팀이 쓰는 지속형 에이전트에도 적합 |
| [Agent Zero](https://github.com/agent0ai/agent-zero) | [v2.13 · 9월 24일](https://github.com/agent0ai/agent-zero/releases/tag/v2.13) | Linux 데스크톱, 브라우저, 문서 공동 편집, 프로젝트별 설정·기억, 파일 복구 | **컴퓨터 업무 비교 후보.** GUI와 문서 작업 비중이 높을 때 유력 |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | [0.7.20 · 9월 30일](https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.20) | 계획·하위 에이전트·파일·기억·도구 승인·체크포인트가 포함된 실행 라이브러리 | 자체 제품에 엔진을 심을 때 유력. 업무용 화면·고객 운영 기능은 추가 필요 |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | [0.2.0-rc.2 · 9월 29일, 프리릴리스](https://github.com/deepseek-ai/deepseek-harness/releases) | 플러그인으로 교체하는 실행 구조, 웹·데스크톱 UI, SDK, 세션 저장 | 유망한 확장 기반. 공식적으로 개발자 프리뷰와 호환성 변경을 예고해 주력 채택은 보류 |
| [OpenClaw](https://github.com/openclaw/openclaw) | [v2026.9.6 · 9월 24일](https://github.com/openclaw/openclaw/releases/tag/v2026.9.6) | 메신저·기기 연결, Gateway, 교체 가능한 모델·실행기·플러그인 | 여러 채널에서 전문가에게 일을 맡기는 접점이 핵심일 때 유력 |

이 여섯 후보의 루트 코드는 MIT다. 저작권·라이선스 고지 보존 조건이 있고, 포함된 별도 패키지와 모델·외부 서비스의 조건은 따로 적용된다. 원문: [DeerFlow](https://github.com/bytedance/deer-flow/blob/main/LICENSE), [Hermes](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE), [Agent Zero](https://github.com/agent0ai/agent-zero/blob/main/LICENSE), [Deep Agents](https://github.com/langchain-ai/deepagents/blob/main/LICENSE), [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/LICENSE), [OpenClaw](https://github.com/openclaw/openclaw/blob/main/LICENSE).

**DeerFlow를 가져오면 재사용할 수 있는 범위가 넓다.** 실행 코어와 서비스 코드가 나뉘어 있고, Python 실행기 위에 FastAPI Gateway와 Next.js 화면이 있다. 직종별로 모델·스킬·도구·하위 에이전트를 설정하는 구조도 있다. 직종이 늘 때마다 실행 시스템 전체를 복제할 필요가 줄어든다는 것이 도입상 장점이다. [아키텍처](https://github.com/bytedance/deer-flow/blob/f9f6a36243bea5c539c63bd22b33a139edbc4b69/docs/ARCHITECTURE.md), [전문 에이전트 설정](https://github.com/bytedance/deer-flow/blob/f9f6a36243bea5c539c63bd22b33a139edbc4b69/backend/packages/harness/deerflow/config/agents_config.py).

소스를 개조할 때의 주요 진입점은 다음과 같다. 경로는 내려받은 [DeerFlow 소스](sources/deer-flow/) 기준이다.

| 붙일 기능 | 기존 코드·설정 위치 | 추가할 내용 |
|---|---|---|
| 직종별 전문가 구성 | `backend/packages/harness/deerflow/config/agents_config.py` | 직종별 모델, 스킬, 도구, 위임 범위 |
| 업무 절차와 업무 시스템 연결 | `skills/public/`, `backend/packages/extension-api/` | 직종별 절차, 근거 조회, 업무 API |
| 고객·업무 기억 | `backend/packages/harness/deerflow/agents/memory/backends/` | 기억의 출처·만료·정정·고객별 접근 범위 |
| 작업 중단과 재개 | `backend/packages/harness/deerflow/runtime/runs/`, `runtime/checkpointer/` | 외부 업무 상태 대조, 중복 실행 방지 |
| 업무 완료 판정 | `backend/packages/harness/deerflow/runtime/goal.py` | 실제 결과물과 외부 처리 결과를 검사하는 직종별 검증기 |
| 정기 업무 | `backend/app/scheduler/` | 직종별 주기와 납품·알림 경로 |

DeerFlow의 내장 완료 판정은 **보이는 대화 내용을 모델이 평가하는 방식**이며, 평가 지시도 코딩 도우미를 전제로 한다. 우리 목적에서는 문서가 실제로 만들어졌는지, 근거가 맞는지, 외부 시스템의 처리가 끝났는지를 따로 확인해야 한다. 이 부분이 전문가 제품으로 바꿀 때의 핵심 추가 기능이다. [완료 판정 구현](https://github.com/bytedance/deer-flow/blob/f9f6a36243bea5c539c63bd22b33a139edbc4b69/backend/packages/harness/deerflow/runtime/goal.py).

운영 설정도 선택에 영향을 준다. 체크포인트는 설정에 따라 메모리·SQLite·Postgres를 쓰므로 재시작 후 이어서 작업하려면 영속 저장을 구성해야 한다. 브라우저 조작 기능은 선택 설치이며 현재 프로세스 내부 세션 때문에 Gateway worker 하나를 요구한다. 예약 작업은 아직 MVP로, 채널별 납품 대상 연결 등이 남아 있다. [체크포인트 코드](https://github.com/bytedance/deer-flow/blob/f9f6a36243bea5c539c63bd22b33a139edbc4b69/backend/packages/harness/deerflow/runtime/checkpointer/provider.py), [브라우저·예약 작업 설명](https://github.com/bytedance/deer-flow/blob/f9f6a36243bea5c539c63bd22b33a139edbc4b69/README.md).

**Hermes에서 특히 볼 것은 경험을 스킬로 남기는 기능이다.** `skill_manage`로 재사용할 절차를 만들거나 수정하고, 사실 기억과 절차 기억을 구분한다. 작업 후 검토와 변경 제안도 지원한다. 다만 이것은 모델의 지능이나 전문가 정확도가 저절로 올라갔다는 증거가 아니다. 우리 시스템에서는 새 절차를 평가용 업무에 적용해 개선과 퇴행을 확인한 뒤 채택해야 한다. [스킬과 자기개선 구조](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

완성형 제품 개조를 택한다면 DeerFlow 하나로 직종 하나를 구현하고, 같은 업무를 Hermes 또는 Agent Zero에 맡겨 비교할 수 있다. Hermes의 경험 축적 기능은 그 비교에서 부족함이 드러나면 이식 후보로 삼는다. 두 실행 시스템을 처음부터 합치면 세션·기억·권한 관리가 중복되고 유지보수 범위가 커질 수 있다. 자체 실행 기반을 조립하는 선택은 [SDK 비교와 구현 범위](상용개발-후보목록.md)를 따른다.

추가 후보들은 다음 용도로 남길 만하다.

| 후보 | 재사용 가치 | 채택 조건·한계 |
|---|---|---|
| [Kortix / Suna](https://github.com/kortix-ai/suna) | 에이전트·스킬·회사 기억·커넥터를 관리하는 제품 구조 | 최신 코드는 **Elastic License 2.0**. 상당한 기능을 제3자에게 제공하는 호스팅·관리형 서비스에 제한이 있다. 고객용 서비스 기반으로 삼으려면 제공 방식과 권한을 먼저 확인해야 한다. [라이선스](https://github.com/kortix-ai/suna/blob/20732efa66ac2d99fe9c08687ec875439957e791/LICENSE) |
| [Dify](https://github.com/langgenius/dify) | 지식 검색과 정형 워크플로를 빠르게 제공하는 제품 | 수정 Apache 2.0 조건에 멀티테넌트와 프런트엔드 표시 제한이 있다. [라이선스](https://github.com/langgenius/dify/blob/216151ffa712914908317f9efceadd894d5af9b0/LICENSE) |
| [OpenHands](https://github.com/OpenHands/OpenHands) | 에이전트 코드를 개발·수정하는 작업자 | 소프트웨어 개발에 초점이 있다. 여러 직종의 업무 서비스 기반과는 역할이 다르다 |
| [Rome](https://github.com/rome-os/rome) | 에이전트가 실행 절차·도구·환경을 확장하는 구조 | [node-core-v0.1.1](https://github.com/rome-os/rome/releases/tag/node-core-v0.1.1) 단계. 주력보다 구조 참고와 소규모 실험에 배치 |
| [OpenFang](https://github.com/RightNow-AI/openfang) | 예약 실행하는 업무 패키지 `Hands`, Rust 기반 서비스 | 업무 패키지 구성이 목적과 닿는다. 최신 확인 릴리스는 [v0.6.9 · 5월 13일](https://github.com/RightNow-AI/openfang/releases/tag/v0.6.9)이며, 아직 1.0 이전이다. 최신 개발 활동은 별도 확인 필요 |
| [AI Manus](https://github.com/Simpleyyt/ai-manus) | 샌드박스에서 도구를 쓰는 범용 에이전트 제품 | [v2.8.0 · 9월 15일](https://github.com/Simpleyyt/ai-manus/releases/tag/v2.8.0)로 개발은 이어진다. 우리 목적에서는 위 후보들과 실제 업무로 비교할 때의 기준선으로 남긴다 |

Kortix는 자체 호스팅에서도 에이전트 세션에 별도 샌드박스 제공자를 사용하는 구조다. OpenClaw는 서로 신뢰하지 않는 고객들을 서비스할 때 고객별 Gateway를 분리하도록 안내한다. 둘 다 설치 가능 여부만으로 고객 서비스 운영이 해결되는 것은 아니다. [Kortix 자체 호스팅](https://github.com/kortix-ai/suna/blob/main/docs/runbooks/self-hosting.md), [OpenClaw 팀 배치](https://docs.openclaw.ai/start/teams).

기반 선택을 확정할 비교 과제는 **자료 수집 → 근거가 있는 결과물 작성 → 중단 후 재개 → 다음 작업에 경험 재사용**을 포함해야 한다. 동일 모델·도구·예산으로 결과물 합격률, 사용자 개입 횟수, 재개 성공률, 비용을 비교하면 된다. 직종별 판단과 별도 평가기를 붙였을 때도 유지보수 부담이 작은 기반을 채택한다.
