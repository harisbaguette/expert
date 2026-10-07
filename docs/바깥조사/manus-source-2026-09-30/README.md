# Manus 코드 확보 결과

확인일: 2026-09-30.

Manus 샌드박스의 공개 덤프와 AI 재구성본을 찾았다. 재구성본은 내려받았다. **최신 Manus 2.0의 Cascade, Cue, Meta Muse의 서버 측 핵심 에이전트 원본은 확보하지 못했다.**

AI로 개조할 수 있는 별도 기반으로 MIT 라이선스의 `Simpleyyt/ai-manus`도 내려받았다. 이 프로젝트를 Manus 공식 원본으로 취급하면 안 된다.

## 내려받은 코드

| 폴더 | 출처와 성격 | 확보한 버전 | 확인 범위 |
|---|---|---|---|
| [manus-open-reconstruction](sources/manus-open-reconstruction/) | [whit3rabbit/manus-open](https://github.com/whit3rabbit/manus-open). 게시자가 Manus 바이트코드를 바탕으로 Claude 3.7을 이용해 재구성했다고 밝힘 | `9b619acaf2605a9de416944ccba838c277b1dfb9`, 기본 브랜치 커밋 2025-03-31 | 65개 파일. Python 53개 파일, 11,460줄. 읽을 수 있는 샌드박스·브라우저 코드 |
| [ai-manus](sources/ai-manus/) | [Simpleyyt/ai-manus](https://github.com/Simpleyyt/ai-manus). 별도 개발자가 구현한 에이전트 제품 | `496547ce6a5f599333138342ec126a7ea8ec9646`, 기본 브랜치 커밋 2026-09-14 | 575개 파일. Python 225개 파일, 27,616줄. 백엔드·프런트엔드·샌드박스 포함 |

`pushed_at`과 기본 브랜치의 마지막 커밋 날짜는 다를 수 있다. 위 날짜는 실제로 내려받은 커밋 기준이다. 원본 ZIP은 [archives](archives/)에 있고, URL·커밋·SHA-256은 [manifest.json](manifest.json)에 기록했다. 소스와 ZIP은 이 폴더의 `.gitignore`로 상위 저장소 추적에서 제외했다.

ZIP CRC, 다운로드 SHA-256, 압축 해제한 각 파일과 ZIP 내용의 일치를 확인했다. Python 파일 278개의 구문 분석은 통과했다. **의존성 설치, 서비스 실행, 제품 기능 검증은 하지 않았다.** 결과는 [verification.json](verification.json)에 있다.

## 재구성본에서 확인한 것

`app/server.py`는 FastAPI로 파일·브라우저·터미널 동작을 제공한다. `start_server.py`도 이 서버를 시작한다. `browser_use/agent/service.py`에는 브라우저 에이전트 루프가 있지만, 이것을 Manus 전체 작업을 지휘하는 비공개 에이전트 엔진과 동일하게 볼 근거는 없다.

| 살펴볼 부분 | 파일 |
|---|---|
| 샌드박스 도구 API | [app/server.py](sources/manus-open-reconstruction/app/server.py) |
| 브라우저 세션·실행 관리 | [browser_manager.py](sources/manus-open-reconstruction/app/tools/browser/browser_manager.py) |
| 터미널 프로세스 관리 | [terminal_manager.py](sources/manus-open-reconstruction/app/tools/terminal/terminal_manager.py) |
| 파일 편집 | [text_editor.py](sources/manus-open-reconstruction/app/tools/text_editor.py) |
| 브라우저 에이전트 루프 | [browser_use/agent/service.py](sources/manus-open-reconstruction/browser_use/agent/service.py) |

복원자는 [직접 작성한 설명](https://github.com/whit3rabbit/manus-open/issues/1#issuecomment-2715948377)에서 복원 과정에 많은 코드가 유실됐고, AI가 누락된 함수를 채웠다고 밝혔다. 따라서 이 자료로 원본의 정확한 동작이나 성능을 입증할 수 없다. 저장소는 보관 상태이며, 내려받은 루트에는 LICENSE 파일이 없고 GitHub의 라이선스 판정도 `null`이다.

## 다른 원본 후보의 판정

| 후보 | 직접 확인한 내용 | 활용 한계 |
|---|---|---|
| [larrykoo711/manus-sandbox-code](https://github.com/larrykoo711/manus-sandbox-code) | 2025년 3월 샌드박스 자료. `sandbox-runtime/app/server.py` 앞부분에 PyArmor 표식이 있음 | 읽을 수 있는 최신 에이전트 원본이 아님. 업로더의 MIT 표시는 Manus 공식 공개 사실을 증명하지 않음 |
| [kiliczsh/manus-sandbox](https://github.com/kiliczsh/manus-sandbox) | 2025년 3월 자료. `opt/.manus/.sandbox-runtime/app/server.py` 앞부분에 PyArmor 표식이 있음 | 실행 환경 덤프 계열. 최신 Cascade나 Cue 코드라는 근거 없음 |
| [phulelouch/manus-sandbox](https://github.com/phulelouch/manus-sandbox) | 설명에 샌드박스 유출본이라고 표기. GitHub 메타데이터의 마지막 push는 2025년 4월 | 원본성·완전성·최신성 확인 안 됨 |
| [jlia0의 Manus tools and prompts](https://gist.github.com/jlia0/db0a9695b3ca7609c9b1a08dcbf872c9) | 에이전트 지시문·도구 정의라고 게시된 문서 | 프롬프트와 인터페이스 자료. 서버 구현 소스가 아니며 공식 진위 보증 없음 |
| [Manus Computer Sandbox 분석](https://gist.github.com/Oanakiaja/f2cc8f52b6a4b75215b67302b0f0c1c1) | 샌드박스 구조와 Nuitka 실행 파일 등에 관한 제3자 관찰 | 소스 저장소가 아님. 이번 조사에서 실제 Manus VM과 대조하지 않음 |
| [manus-ai 공식 조직](https://github.com/manus-ai) | 공개 저장소 5개: MCP 연결 코드 4개, 외부 소스 배포용 저장소 1개 | 확인한 목록에 Cascade·Cue 서버 엔진 없음 |
| [third-party-source-archives의 Releases](https://github.com/manus-ai/third-party-source-archives/releases) | API로 확인한 공개 배포물 6개는 FFmpeg 9.0.1 관련 소스·실행 파일 | Manus 에이전트 엔진 소스가 아님 |

공개 덤프 두 곳의 파일 앞부분만 읽고 PyArmor 여부를 확인했다. 내용은 로컬에 복사하지 않았으며 판정만 [public-dump-inspection.json](public-dump-inspection.json)에 저장했다.

## AI로 개조할 기반

이번에 확보한 두 저장소 중 **제품을 개조하는 출발점으로는 `ai-manus`가 더 적합하다**는 것이 이번 코드 열람의 판단이다. 에이전트 실행 루프와 모델 연결, UI가 함께 있고 루트 LICENSE에 MIT가 명시되어 있기 때문이다. 실행 안정성이나 Muse 수준의 성능까지 확인한 판단은 아니다.

AI에게 아래 순서대로 읽히면 핵심 구현을 빠르게 파악할 수 있다. 기준 폴더는 `sources/ai-manus/backend/app/`이다.

| 목적 | 파일 |
|---|---|
| 계획·실행·실패 후 재계획 | [domain/services/flows/plan_act.py](sources/ai-manus/backend/app/domain/services/flows/plan_act.py) |
| 별도 에이전트 루프 구현 | [domain/services/flows/agent_loop.py](sources/ai-manus/backend/app/domain/services/flows/agent_loop.py) |
| 모델 호출·도구 실행·재시도 | [domain/services/agents/base.py](sources/ai-manus/backend/app/domain/services/agents/base.py) |
| 대화 기록·컨텍스트 크기 관리 | [domain/models/memory.py](sources/ai-manus/backend/app/domain/models/memory.py) |
| 모델 API 연결 | [infrastructure/external/llm/openai_llm.py](sources/ai-manus/backend/app/infrastructure/external/llm/openai_llm.py) |
| Docker 실행 환경 | [infrastructure/external/sandbox/docker_sandbox.py](sources/ai-manus/backend/app/infrastructure/external/sandbox/docker_sandbox.py) |
| 기능 패키지 로딩·동기화 | [application/services/skill_runtime_service.py](sources/ai-manus/backend/app/application/services/skill_runtime_service.py) |

여기서 `Memory`는 대화 컨텍스트 관리 구현이다. Muse와 같은 장기 개인 기억이나 자동 자기 개선을 이미 구현했다고 추정하면 안 된다.

## 최신판과 인용문에서 남은 불확실성

[Manus의 2026-09-28 발표](https://manus.im/blog/introducing-manus-2-0)는 Cascade를 자체 에이전트 실행 구조로 설명하고, Cue가 같은 기반 시설을 사용한다고 밝힌다. 이번에 확보한 2025년 샌드박스 재구성본을 그 최신판으로 볼 수 없다.

사용자가 인용한 “Meta 전 동료, 陳 성 엔지니어, 0.5명 인력, Manus 코드를 AI로 개조했다”는 이야기의 원글이나 직접 증거는 찾지 못했다. 중국어·영어의 해당 인명 단서와 인력 표현으로 검색했으나 작성자·게시 시점을 특정하지 못했다. 이 결과는 그 이야기가 거짓이라는 판정이 아니다. 원문 URL 또는 작성자 계정이 있어야 다음 확인을 좁힐 수 있다.

설계 비교에는 [Manus 창업자의 컨텍스트 엔지니어링 글](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)과 [Meta의 Muse 기술 설명](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)을 사용할 수 있다. 설계 설명을 읽는 것과 해당 제품의 원본 코드를 확보하는 것은 구분해야 한다.
