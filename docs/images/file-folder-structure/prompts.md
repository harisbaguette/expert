# 파일·폴더 구조 일러스트 제작 기록

현재 사용본은 **2026-10-23 3차 수정본**이다. 현재 본문과의 대조, 수정 프롬프트와 생성 원본은 아래 [2026-10-23 3차 갱신](#2026-10-23-3차-갱신)에 기록했다. 그 앞의 [2026-10-23 2차 갱신](#2026-10-23-2차-갱신)과 [2026-10-23 갱신](#2026-10-23-갱신)은 2차·1차 수정 이력이다. 앞의 2026-10-22 기록은 최초 제작 이력이다.

제작일: 2026-10-22. 내장 `image_gen`으로 생성·수정했다. 외부 AI CLI·API와 외부 다운로드 에셋은 사용하지 않았다.

사용 문서: [파일·폴더 구조](../../../파일-폴더-구조.md). 문서에 적힌 목표 구조를 설명하며 실제 운영 폴더를 구축하거나 자료를 이동한 결과가 아니다.

기존 `docs/images/expert-implementation/factory-implementation-overview.png`와 `memory-state.png`를 직접 보고 하늘색·연노랑·짙은 윤곽선의 설명 그림체를 맞췄다. 최초 생성에는 참조 이미지를 입력하지 않았고, 수정에는 이번 생성 원본만 입력했다. 기존 공장·기억 그림은 주제가 달라 이 문서의 구조 설명에 그대로 재사용하지 않았다.

그림은 역할과 포함 관계를 읽기 쉽게 줄였다. `snapshots/`, `sessions/`, `deliveries/` 등 일부 경로의 개별 ID와 세부 파일은 생략했으며, 전체 경로는 본문의 텍스트 트리를 따른다. 두 번째 그림 하단의 관리 폴더 다섯 개는 운영 저장소의 같은 최상위 경로를 묶어 표시한 것이다.

## storage-locations

결과: [storage-locations.png](storage-locations.png)

최초 생성 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-157671bf-f5be-405d-aca9-406e12f6ccd9.png`

채택한 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-157671bf-f5be-405d-aca9-406e12f6ccd9.png`

### 생성 프롬프트

```text
Use case: infographic-diagram.
Create one finished Korean explanatory illustration for a file/folder architecture document, landscape 3:2, high-resolution opaque white background. Match a friendly professional Japanese explanatory manual: confident clean charcoal outlines, sky-blue folder illustrations, restrained soft yellow accents, a few natural adult office characters only when they explain an action. Flat hand-drawn illustration, NOT a software screenshot or a text slide. Excellent Korean typography, English path labels rendered verbatim. Spacious composition, no gradients, no decorative sparkles, no section numbers, no logos. Short labels only. This is a PROPOSED TARGET architecture, not already implemented.

Large title exactly: "작성 · 설치 · 보관을 나눈다". Small meaningful status label: "목표 구조".

Upper two-thirds: three equally important roomy scenes from left to right.
LEFT: An author organizing two open folders on a workbench, heading "만드는 곳", path "expert-factory/". The two folders are "knowledge/" with the short explanation "분야 지식·실무서", and "experts/" with "전문가 구성". Visually these are authored definitions/configurations, not customer documents.
MIDDLE: Installed, checked software package on a computer, heading "실행하는 곳", path "install_root", short label "검사한 프로그램·구성". Small lock/read icon labelled "업무 실행은 읽기 전용".
RIGHT: A substantial archive cabinet containing source books, customer folders and a database cylinder, heading "자료를 보관하는 곳", path "knowledge_root", short label "원본·고객 업무·대화·DB".

Between LEFT and MIDDLE, exactly ONE simple right-pointing blue arrow labelled "검사 후 설치".
Between RIGHT and MIDDLE, exactly ONE simple left-pointing blue arrow labelled "허용된 자료 읽기". This is a read/reference connection, not moving or copying the whole archive. Keep arrows in clear gaps, no crossings.

Bottom third: three physically separate small illustrated facilities, with generous white space and no connection arrows implying public access.
A locked exam cabinet: "evaluation_root", "보호된 시험·정답", small label "평가 담당".
A protected management ledger with a key: "control_root", "삭제·권한 철회 기록", small label "관리 담당".
An external backup drive clearly separate from the main archive hardware: "backup_target", "DB·파일 백업", small label "다른 장치·저장 서비스".
These are access/storage roles, not necessarily six separate servers. The image must communicate the distinction between authored source, installed release, operating data, protected evaluation, independent control records, and off-device backup without a wall of text. Use all exact labels above and no additional explanatory paragraphs. Make all labels legible in a document at 1000px width.
```

### 실제 이미지 확인

작성 원본, 설치 판본, 운영 저장소와 보호 시험·관리 기록·외부 백업의 역할을 구분했다. 검사 후 설치 화살표와 자료 읽기 화살표의 방향, 목표 구조 표기를 실제 이미지에서 확인했다.

## knowledge-root

결과: [knowledge-root.png](knowledge-root.png)

최초 생성 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-6eb4e2b2-e95e-42d2-891f-88f6a56f4ba2.png`

채택한 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-274e6a12-7036-4ce8-8910-0a75e29c7fb1.png`

### 생성 프롬프트

```text
Use case: infographic-diagram.
Create one finished Korean educational illustration explaining a directory hierarchy. Landscape 3:2, high-resolution, opaque pure white background. Clean hand-drawn editorial illustration in a friendly Japanese explanatory manual style, charcoal outlines, sky-blue folders and pale yellow restricted folders, simple books and documents, restrained detail. No 3D, no gradients, no logos, no decorative people or sparkles. Korean text must be correct; path names must be exact. The graphic must be an understandable illustrated directory tree, not merely a table or software screenshot.

Title: "운영 자료는 이렇게 보관한다".
At top center under title, a large parent folder marked "knowledge_root". A clean branching line from this parent connects the THREE prominent archive groups across the middle. NO arrows between the three groups.

LEFT group: heading "공통 자료". An open blue archive folder labelled "shared/" containing a smaller shelf labelled "collections/". Inside this shelf, show three tidy smaller folders with paired short labels:
"objects/" — "원본·확정 파일"
"derived/" — "가공 자료"
"exports/" — "내보낸 사본".
An unobtrusive book spine may say "법령·판례".

MIDDLE group: heading "이용이 제한된 자료". A yellow archive folder with a lock. Path displayed as two accurate lines "restricted/<scope-id>/" then "collections/". Within it three smaller folders:
"objects/" — "원본·확정 파일"
"derived/" — "가공 자료"
"exports/" — "내보낸 사본".
The lock means contract/subscription access restrictions, not an encrypted format.

RIGHT group: heading "고객 업무". A blue customer folder labelled "tenants/<tenant-id>/". INSIDE it, visibly nested, a lockable compartment labelled "scopes/<scope-id>/". Label this compartment "열람 범위별". INSIDE that compartment show FOUR smaller folders:
"objects/" — "원본·확정 파일"
"derived/" — "가공 자료"
"exports/" — "내보낸 사본"
"cases/" — "업무별 폴더".
It is CRITICAL that objects, derived, exports, cases are inside scopes, NOT loose directly under tenants. Do not place collections under the customer scope. The customer's original files are not automatically shared. No crossing links or arrows between customers, shared and restricted.

Bottom of image: a compact open shelf labelled "같은 저장소의 관리 폴더", clearly a sibling set under knowledge_root, not children of cases. Connect it with one clean outer branch from the ROOT, keeping all lines clear of labels. Five small illustrated folders/bins in one row, each with its exact label and short role:
"config/" — "설정"
"staging/" — "접수·검사 중"
"cache/" — "재생성 가능"
"stores/postgres/" — "DB"
"operations/" — "운영 기록".
All eight top-level branches belong to knowledge_root. The three big groups are expanded; the five management folders are compact. There is NO temporal arrow between folders. Containment and branch lines show structure. Keep whitespace and clear distinct nesting; do not add slogan/footer text. Give each role enough room to read comfortably at 1100px document width.
```

### 수정 프롬프트

```text
Edit this existing illustrated folder hierarchy. Preserve the title, all artwork, three-column layout, colors, crisp text, all customer nesting, the five management folders and whitespace. Make ONLY these two directory accuracy corrections:
(1) The management shelf at the bottom currently looks like a child of the MIDDLE restricted folder, because a vertical line exits its bottom. REMOVE that outgoing vertical line below the middle yellow group, and remove the redundant bracket above the bottom shelf. Connect the bottom management shelf DIRECTLY to the top knowledge_root branch using a clean outside route: extend the upper root branch to the FAR LEFT in the white margin, descend outside the left common-data frame, then turn right into the LEFT border of the bottom management shelf. This must never touch or pass through any of the three archive group frames. Ensure the outer line has comfortable margin from image edge, adjusting the three groups inward a few pixels if necessary. Keep the root's three existing valid branches to common, restricted and customer groups. There must be no connecting line from restricted to management.
(2) Each collection is an intermediate directory. In the LEFT group replace the label "collections/" with "collections/<collection-id>/", widening its label as needed while keeping it legible. In the MIDDLE group retain first path line "restricted/<scope-id>/" and replace the second line "collections/" with "collections/<collection-id>/". Leave the three inner folders objects/ derived/ exports/ as they are; these belong within the named collection.
No other text or relation changes. Clean deliberate line routing and correct containment matter most. Final finished illustration.
```

### 실제 이미지 확인

관리 폴더를 knowledge_root에서 직접 연결하도록 고쳤다. collections/<collection-id>/ 단계를 보완했고, 고객의 objects/·derived/·exports/·cases/가 scopes/ 안에 들어가는 것을 실제 이미지에서 확인했다.

## case-folders

결과: [case-folders.png](case-folders.png)

최초 생성 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-bbdc4f87-c485-4bb0-9831-af7effb46ff9.png`

채택한 원본: `/Users/haris/.codex/generated_images/01a16260-7fc8-70f2-b8ff-61ae6792adb4/exec-e8f885c9-2d7a-4411-998c-a703a0145a42.png`

### 생성 프롬프트

```text
Use case: infographic-diagram.
Create one finished Korean educational illustration explaining one job's working folders. Landscape 3:2, high-resolution white opaque background. Same friendly professional hand-drawn explanatory-manual style: confident charcoal linework, sky-blue folders, restrained pale yellow highlights, natural adult worker checking a document only where useful. No 3D, gradients, decorative sparkles, logos or wall of text. Large crisp Korean labels and verbatim English filenames.

Title: "업무 한 건의 폴더를 열어 보면".

At upper left, a locked parent archive label "scopes/<scope-id>/", and inside it a large wide blue tabbed folder boundary labelled "cases/<case-id>/". This large case boundary contains exactly FOUR sibling folders across the page, in this order. A simple tree branch or clear nested containment shows that all four are siblings, NOT sequential steps.
1. "snapshots/" — short Korean name "실행 기준". Inside, a frozen/pinned plan document labelled "고정한 계획·입력".
2. "sessions/" — short Korean name "지속 대화". Inside, two little subfolders "sdk/" labelled "대화 기록", and "cwd/" labelled "허용된 작업 경로". Depict a conversation notebook. Never imply these are temporary.
3. "work/<run-id>/" — short Korean name "작업 공간". Inside, three subfolders:
"input/" with a small lock and label "읽기 전용";
"output/" with a pencil and label "미확정 결과";
"tmp/" with a scrap bin and label "임시 파일".
4. "deliveries/" — short Korean name "납품 묶음". Inside, a checklist document "manifest.json" and a zipped parcel "package.zip". Clearly show a checked/selected bundle, not all work files.

Below the large CASE boundary but still within the surrounding SCOPE context, draw a simple horizontal file-finalization sequence:
a work-result sheet labelled "output/" -> a human inspecting it with a magnifier labelled "검사·확정" -> an archive folder labelled "objects/" with short explanation "원본·확정 결과" -> a neat delivery parcel labelled "deliveries/".
The final arrow to the delivery parcel is labelled "허용된 파일만".
IMPORTANT: objects/ is a SIBLING of cases/ under the same scope, NOT a child of cases/. The bottom row is a process illustration, not an additional copy of the four-folder hierarchy. Make that distinction clear with a small heading "결과를 확정할 때". Do not draw raw output directly into deliveries bypassing inspection.

At upper right OUTSIDE the scope folder enclosure, a separate PostgreSQL database cylinder marked "DB", with three short lines "권한", "계획·진행 상태", "파일 ID·판본". Short nearby label "현재 상태의 기준".
Do not draw DB as a child of cases or scope. No arrow implying that changing a JSON file sets job completion. Omit run-specific IDs and paths beyond the exact labels requested to avoid clutter. Maintain generous spacing, legible technical text, no crossing lines, no extra paragraphs. Final artwork should make it immediately clear where fixed inputs, persistent conversations, temporary work, final bytes and deliverable bundles belong.
```

### 수정 프롬프트

```text
Edit this existing explanatory illustration, preserving the entire title, four case subfolders and their contents, the separate DB cylinder, bottom output → inspection → objects → deliveries process, all wording, drawing style and colors. Make ONE focused structural clarification: add one small blue folder labelled exactly "objects/" as a SIBLING of the large cases/<case-id>/ folder INSIDE the outer scopes/<scope-id>/ enclosure. There is a white horizontal band to the RIGHT of the cases/<case-id>/ tab, between the top outer scope border and the top border of the large case content area. Place the small objects/ folder in that band near the right side, at the same hierarchy level as the cases tab. It must sit completely INSIDE the outer scope border and completely OUTSIDE the inner case border, with clear whitespace from both. If necessary move the inner case content area down slightly or adjust the band height so the small folder is not touching any border. Keep all four case contents comfortably legible. Do not place this added objects/ inside deliveries or any of the four subfolders. Do not add arrows from objects to the DB. It is okay that objects also appears again in the separate bottom finalization process; that bottom row explains behavior. Add no explanatory sentence or new path labels. This edit must make it visibly clear that original/confirmed bytes live beside the case folder within the same access scope.
```

### 실제 이미지 확인

objects/를 cases/와 같은 scope의 형제 폴더로 표시했다. 고정 계획, 지속 대화, 읽기 전용 입력, 미확정 출력, 임시 파일, 납품 묶음과 별도 DB를 구분했다. 검사·확정 후 objects/에 보관하고 허용된 파일만 납품하는 흐름을 확인했다.



## 2026-10-23 갱신

현재 `파일-폴더-구조.md`와 `공장 구현 설계.md`를 읽고 기존 네 장을 내장 `image_gen`으로 각각 편집했다. 편집 입력은 이 프로젝트가 보유한 기존 그림이며, 외부 다운로드나 합성 에셋은 사용하지 않았다. 수정 결과를 재압축하지 않고 기존 이미지 경로에 복사했다. 본문에서는 대체 설명만 갱신했다.

### storage-locations

- 적용 파일: `docs/images/file-folder-structure/storage-locations.png`
- 생성 원본: `/Users/haris/.codex/generated_images/01a16613-0859-7242-b180-7aab956df091/exec-52037cae-e242-4d4f-82e6-d94216649874.png`
- 반영·확인: 작성・설치·운영의 역할을 분리했다. install_root를 실행 주체처럼 보이게 하던 자료 읽기 화살표를 없애고, test_root·평가 계정·관리 계정·PC 밖 백업을 표시했다.

```text
Edit this existing Korean file-storage architecture illustration to match the revised design. Keep the established polished flat explanatory-manual style, charcoal outlines, pale sky blue and restrained yellow, white background, adult office character, large legible Korean. Landscape 3:2 high resolution. Redraw/reflow as needed for the following content, without cramming. No decorative title underline or slogan.

Title: "작성 · 설치 · 운영을 나눈다". Small status label "목표 구조".
Upper 60% has THREE main roles:
LEFT "작성 원본", path "expert-factory/": author at desk with folders for "코드", "지식·실무서", "전문가 구성". Short Git label "Git".
MIDDLE "설치 판본", path "install_root": checked installed software package and lock, label "검사한 프로그램·구성", second short label "업무 계정은 읽기만".
RIGHT "운영 자료", path "knowledge_root": archive with original books, customer folders, protected conversation notebook and one DB cylinder. Short label "원본·업무·대화·실행 기록·DB".
The ONLY upper arrow is LEFT to MIDDLE, labelled "검사 후 설치". Remove the old arrow from storage toward install: install_root is an installed read-only location, not the process performing data access. Do not connect the three roles with misleading process arrows.

Bottom 35% has FOUR clearly distinct illustrated roles, all outside knowledge_root. No enclosing shared data container.
1 "test_root": small test bench/computer with isolated data cylinder, "시험 전용 DB·파일".
2 "evaluation_root": locked answer cabinet, "보호 시험·정답", small "평가 계정".
3 "control_root": protected ledger/key, "삭제·철회·업데이트 이력", small "관리 계정".
4 "backup_target": external drive and cloud, "DB·파일·보호 이력", small "PC 밖 · 덮어쓰기 방지".
All text verbatim, clear spacing. The bottom four paths are distinct roots, not subdirectories of knowledge_root. These are roles on an initial single PC plus off-device backup, not seven required servers. Exclude extra fine print. Preserve the friendly diagrammatic folder style with correct hierarchy.
```

### knowledge-root

- 적용 파일: `docs/images/file-folder-structure/knowledge-root.png`
- 생성 원본: `/Users/haris/.codex/generated_images/01a16613-0859-7242-b180-7aab956df091/exec-f5a8d1e7-84b6-48c4-bddd-066701bb2afc.png`
- 반영·확인: browser-profiles/를 tenants/ 안에서 scopes/와 같은 단계로 추가했다. staging/과 cache/의 scope-id, operations/의 상태·수치 전용 역할, 관리 폴더의 루트 직속 관계를 확인했다.

```text
Edit this Korean illustrated folder tree. Preserve title "운영 자료는 이렇게 보관한다", all exact directory names, white background, charcoal outlines, blue/yellow folders, the three main data groups and bottom management shelf. Reflow only enough to add the missing directories legibly. Landscape 3:2 high resolution.

Required hierarchy:
knowledge_root branches separately to shared/, restricted/<scope-id>/, tenants/<tenant-id>/ AND the bottom same-root management shelf. Keep the outer line that connects the bottom shelf directly to knowledge_root; NEVER connect it through restricted/.
shared/: collections/<collection-id>/ contains objects/ "원본·확정 파일", derived/ "가공 자료", exports/ "내보낸 사본". Preserve.
restricted/<scope-id>/: collections/<collection-id>/ contains the same three. Preserve.
Right "고객 업무" group under tenants/<tenant-id>/ must now contain TWO visibly separate siblings:
- A small horizontal locked folder "browser-profiles/" with short label "계정별 로그인 · 백업 제외". This sits INSIDE tenants but OUTSIDE scopes, ABOVE the scopes compartment. It represents encrypted customer-account browser state, not a public browser history.
- The existing larger "scopes/<scope-id>/" compartment with label "열람 범위별". Inside are objects/, derived/, exports/, cases/ and their existing labels. No collections here.
Make the right group a little taller or the entire tree more compact vertically as needed, while keeping all labels readable.

Bottom five folders remain siblings directly under knowledge_root:
"config/" label "설정"
Change "staging/" to TWO lines "staging/" and "<scope-id>/", label "접수·검사 중"
Change "cache/" to TWO lines "cache/" and "<scope-id>/", label "재생성 가능"
"stores/postgres/" label "DB"
"operations/" label "상태·수치만".
staging and cache are scope-specific. operations stores identifiers/status/metrics only, not sensitive content or full traces. Full run traces are in customer cases, do not add them at root.
No arrows between public, restricted and customer data. Do not imply customer data is shared. No new paragraph or footer. All technical paths are case-sensitive verbatim, including hyphens and angle brackets.
```

### case-folders

- 적용 파일: `docs/images/file-folder-structure/case-folders.png`
- 생성 원본: `/Users/haris/.codex/generated_images/01a16613-0859-7242-b180-7aab956df091/exec-022b8229-9ce8-42e9-a09d-73098ff6941a.png`
- 반영·확인: cases/ 아래에 traces/를 추가하고 work/ 안에 logs/를 추가했다. 지속 대화·보호 실행 기록·도구 출력 로그를 구분했다. objects/와 cases/의 형제 관계를 유지하고 검사·확정 → objects/ → 별도 저장소 보관 확인 → 납품 묶음 순서를 표시했다.

```text
Update this Korean illustrated job-directory diagram to the revised source. Keep its friendly explanatory-manual illustration, white background, blue folders, yellow accents, clean charcoal outlines and natural adult inspector. Landscape 3:2 high resolution. Redraw/reflow into five columns with readable text. Title remains "업무 한 건의 폴더를 열어 보면".

At top a protected "scopes/<scope-id>/" outer folder contains two sibling items: the small "objects/" folder OUTSIDE a wide inner "cases/<case-id>/" folder. Preserve that nesting: objects is NOT inside cases. A separate small DB cylinder at top RIGHT stays entirely OUTSIDE scope; label "DB" and "현재 상태의 기준", with compact "권한 · 계획 · 상태 · 판본".

The inner case folder now contains exactly FIVE sibling folders. These are not sequential workflow steps; use a simple branch line without arrowheads. Use these short path names, individual snapshot/conversation/run/delivery IDs may be omitted:
1 "snapshots/" with heading "실행 기준", pinned document, label "고정한 계획·입력·환경".
2 "sessions/" with heading "지속 대화", encrypted notebook with lock and two subfolders "sdk/" labelled "대화 기록" and "cwd/" labelled "허용 작업 경로". This is persistent, not temporary.
3 NEW "traces/" with heading "보호 실행 기록", locked ledger with three short text lines "모델 입력·응답", "도구 호출·결과", "관리 프로그램만 기록". This is separate from logs/ and work/. Never add a successful checkmark claiming already implemented.
4 "work/" with heading "실행별 작업", four clearly named internal subfolders in a compact 2x2 arrangement: "input/" with lock and "읽기 전용"; "output/" with pencil and "미확정 결과"; "tmp/" with wastepaper and "임시 파일"; NEW "logs/" with terminal page and "도구·SDK 출력". All four inside work. Make this column wider than others as needed.
5 "deliveries/" with heading "납품 묶음", checklist labelled "manifest.json" and package labelled "package.zip".

Below the entire hierarchy is a clearly separate process strip titled "결과를 확정할 때". It has this exact left-to-right workflow, each blue arrow ending at the correct item:
"output/" sheet -> human magnifier "검사·확정" -> "objects/" archive -> off-device backup/checkpoint icon "별도 저장소 보관 확인" -> "deliveries/" parcel.
Small label over the last arrow "허용된 파일만".
The backup checkpoint must be between the confirmed archive and delivery. No direct output-to-delivery bypass. Deliveries is a prepared bundle, not evidence that sending/acceptance has occurred. Preserve generous margins, no border touching letters, all Korean and English correctly spelled. Do not add explanatory paragraphs.
```

네 장 모두 1536×1024px PNG이며, 생성 결과와 1100px 폭의 headless Chromium 표시를 직접 확인했다. 한글·기술 식별자·포함 관계·화살표·잘림을 확인했다. 그림에서 생략한 개별 ID와 세부 설정 파일은 본문의 정확한 텍스트 트리를 따른다. 실제 공장 구현이나 자료 이전 완료를 뜻하지 않는다.

## 2026-10-23 2차 갱신

`파일-폴더-구조.md`의 바뀐 트리(2·3·4·8·10·11절)와 1차 수정본 세 장을 대조해 다른 곳만 고쳤다. `~/.claude/bin/codex-image`(Codex 이미지 생성)로 1차 수정본을 `--ref` 입력으로 주어 편집했다. 외부 다운로드 에셋은 쓰지 않았다. 채택 원본을 재압축하지 않고 기존 경로에 복사했다. 본문에서는 대체 설명만 고쳤다.

분류 대기 범위는 고객 `scopes/` 아래의 범위 하나이고 별도 폴더 경로가 없어 그리지 않았다. `install_root/experts/`의 `playbook.yaml`·`tools.yaml`·`evaluation.yaml`은 세 그림 어디에도 파일 단위로 그리지 않으며, "검사한 프로그램·구성"·"전문가 구성" 요약과 어긋나지 않는다.

### storage-locations

- 적용 파일: `docs/images/file-folder-structure/storage-locations.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16661-d0e2-7f40-8dcd-7d5d5ba5d3d4/exec-7fb0ff75-bdb7-4e91-b6da-9ecdfca050f7.png`
- 고친 곳: `expert-factory/`에 `principles/`·`policies/`를 뜻하는 "기본 지시·권한" 폴더를 더했다. `control_root`를 `revocations/`·`blocklists/`·`update-trust/`·`audit-checkpoints/`에 맞춰 "철회 기록 · 차단 목록 / 업데이트 신뢰 · 감사 확인점"으로 바꿨다. 본문 2절의 비밀 저장소를 다섯째 칸으로 더했다.

```text
Edit the attached existing Korean explanatory illustration about storage roles. Keep everything else identical: title "작성 · 설치 · 운영을 나눈다", the "목표 구조" tag, the flat Japanese explanatory-manual style (confident charcoal outlines, sky blue, restrained pale yellow, white background), the author character, the Git badge, the single blue arrow "검사 후 설치", and the install_root and knowledge_root panels with all their labels unchanged. Landscape 3:2, 1536x1024.

Make ONLY these changes:
1. LEFT panel "작성 원본 / expert-factory/": the desk now holds FOUR folder cards instead of three, in this order: "코드", "지식·실무서", "전문가 구성", "기본 지시·권한". Give the fourth card a simple document-with-shield icon. Shrink the four cards evenly so all fit inside the panel with whitespace; keep the character and Git badge.
2. Bottom row: change from four to FIVE equal panels, all separate locations outside knowledge_root, no arrows between them. Order: test_root, evaluation_root, control_root, backup_target, 비밀 저장소.
 - test_root, evaluation_root, backup_target: keep illustration and labels verbatim.
 - control_root: replace the text "삭제·철회·업데이트 이력" with two short lines "철회 기록 · 차단 목록" and "업데이트 신뢰 · 감사 확인점". Keep "관리 계정".
 - NEW fifth panel at far right, header "비밀 저장소" (Korean header, no path): a small locked key vault with a key card. Label "키·토큰·인증정보", second label "운영 PC · 따로 암호화 백업".
No new title, subtitle, footer or paragraph. Every Korean word spelled exactly; English paths verbatim lowercase with underscores. No text touching panel edges or cut off.
```

### knowledge-root

- 적용 파일: `docs/images/file-folder-structure/knowledge-root.png`
- 1차 생성 원본(글자 작음, 미채택): `/Users/haris/.codex/generated_images/01a16661-d0e2-7fa2-acfd-7ee60a496361/exec-07446e84-ae6c-46cc-9375-3ee83c0d50bd.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16664-64c0-7ab1-973f-b19d35e17594/exec-4483de5b-826d-4318-a633-db19be64b2c6.png`
- 고친 곳: 루트 직속 `joint-scopes/<scope-id>/`와 `offices/<office-id>/browser-profiles/`를 오른쪽 바깥 선으로 `knowledge_root`에 이었다. 고객 범위의 `objects/`를 `objects/<key-id>/`로, `tenants/` 안 `browser-profiles/`의 이름표를 "고객 계정 로그인 · 백업 제외"로 바꿨다. 1차 생성본은 1100px 폭에서 고객 범위 글자가 너무 작아 2차 편집으로 키웠다.

```text
Edit the attached Korean illustrated folder tree "운영 자료는 이렇게 보관한다". Preserve the title, the knowledge_root parent folder, the style (charcoal outlines, sky-blue folders, pale yellow restricted folders, white background), the LEFT "공통 자료" group and the MIDDLE "이용이 제한된 자료" group with all their labels, and the bottom "같은 저장소의 관리 폴더" shelf with its five folders and labels exactly. Landscape 3:2, 1536x1024. Make the three top groups a little shorter to free vertical room.

Changes:
1. RIGHT group "고객 업무" (tenants/<tenant-id>/): keep the browser-profiles/ compartment but change its small label to "고객 계정 로그인 · 백업 제외". Keep the scopes/<scope-id>/ compartment with "열람 범위별" and its four inner folders, but change the first inner folder path from "objects/" to "objects/<key-id>/" with label "키별 원본·확정". Keep derived/ "가공 자료", exports/ "내보낸 사본", cases/ "업무별 폴더".
2. ADD a new band between the three top groups and the bottom shelf, on the right half under the 고객 업무 group, with a heading pill "여러 고객에 걸친 것". It holds TWO compact locked blue folders that are DIRECT children of knowledge_root (siblings of tenants/, NOT inside tenants):
 - "joint-scopes/<scope-id>/" with label "공동 범위 · scopes와 같은 구조"
 - "offices/<office-id>/" containing a small inner folder "browser-profiles/", label "사무소 공용 계정 로그인 · 백업 제외"
 Connect this band to knowledge_root with one clean outer line along the RIGHT margin, mirroring the existing left outer line. The line must not pass through any group frame or label.
3. Keep the existing left outer line from knowledge_root to the bottom management shelf.
All technical paths verbatim and case-sensitive, including hyphens, underscores and angle brackets. No new paragraph, subtitle or footer. No text cut off or touching borders.
```

2차 편집(1차 생성 원본 입력):

```text
Edit the attached Korean illustrated folder tree. Keep every element, word, path, line, color and position the same, EXCEPT improve legibility in the RIGHT "고객 업무" group:
The four inner folder labels inside scopes/<scope-id>/ ("objects/<key-id>/", "derived/", "exports/", "cases/") and their Korean labels ("키별 원본·확정", "가공 자료", "내보낸 사본", "업무별 폴더"), plus the browser-profiles/ label "고객 계정 로그인 · 백업 제외", are too small. Make these texts about 30 percent larger, the same size as the labels in the LEFT "공통 자료" group. To make room, widen the RIGHT group to the left by narrowing the LEFT and MIDDLE groups slightly (their folders and text stay readable and unchanged in wording), and make the four inner folders wider. "objects/<key-id>/" must fit on one line inside its folder card without touching the edge.
All paths verbatim and case-sensitive with hyphens, underscores and angle brackets. Keep the right outer line to the "여러 고객에 걸친 것" band and the left outer line to the bottom management shelf exactly as they are. No new text.
```

### case-folders

- 적용 파일: `docs/images/file-folder-structure/case-folders.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16661-d0e2-7851-b84a-1996f2e6d4ba/exec-405c2c60-6357-4410-916c-39318646ca0d.png`
- 고친 곳: 범위 안의 `objects/`와 아래 흐름의 `objects/`를 `objects/<key-id>/`로 바꿨다. 다른 글자와 배치는 그대로다.

```text
Edit the attached Korean illustration "업무 한 건의 폴더를 열어 보면". Preserve everything — layout, drawing style, colors, all five case subfolders and their text, the DB cylinder and its labels, the bottom process strip and all its text — EXCEPT these two label changes:
1. The small folder at the top right inside the scopes/<scope-id>/ enclosure currently reading "objects/" must read "objects/<key-id>/". Widen that small folder a little to fit; it stays fully inside the outer scope border and fully outside the cases/<case-id>/ border.
2. In the bottom process strip, the folder currently labelled "objects/" must read "objects/<key-id>/" (two lines allowed: "objects/" above "<key-id>/").
No other changes. Text verbatim, angle brackets and hyphen exact, nothing cut off.
```

세 장 모두 1536×1024px PNG다. 원본 크기와 1100px 폭 headless Chromium 표시를 직접 열어 한글·경로 글자, 포함 관계, 선 경로, 잘림·겹침을 확인했다.

## 2026-10-23 3차 갱신

`파일-폴더-구조.md`의 바뀐 트리(3·4·9·10·11절)와 2절 위치 표를 2차 수정본 세 장과 대조해 다른 곳만 고쳤다. `~/.claude/bin/codex-image`로 2차 수정본을 `--ref` 입력으로 주어 편집했다. 외부 다운로드 에셋은 쓰지 않았다. 채택 원본을 재압축하지 않고 기존 경로에 복사했다. 본문에서는 대체 설명만 고쳤다.

그리지 않은 것: `tenants/unassigned/`는 본문 트리에 없고 11절 이전 표에만 나오는 `tenants/<tenant-id>/`의 한 값이라 따로 그리지 않았다. `test_root/`의 `inbox/`·`outbox/`·`mocks/`·`runs/`, `evaluation_root/attacks/`, `install_root/`의 `tools/`·`allowed-scope.json`은 첫 그림의 칸 이름표("시험 DB · 파일 · 모의 시스템", "공격 시험", "도구")로만 요약했다. 폴더 경로는 본문 트리를 따른다.

### storage-locations

- 적용 파일: `docs/images/file-folder-structure/storage-locations.png`
- 채택 원본: `/Users/haris/.codex/generated_images/file-folder-structure-2026-10-23c/storage-v1.png`
- 고친 곳: "설치 판본" → "설치 버전", install_root 이름표 → "프로그램 · 구성 · 도구 · 모델", 넷째 폴더 카드 "기본 지시·권한" → "행동 원칙·권한", test_root에 "시험 DB · 파일 · 모의 시스템"과 "시험 계정", evaluation_root에 "공격 시험", control_root "철회 기록 · 차단 목록" → "삭제·사용 중지 기록", backup_target "DB · 파일 · 보호 이력" → "DB · WAL · 파일 백업".

```text
Edit the attached existing Korean explanatory illustration about storage roles. Keep everything else identical: title "작성 · 설치 · 운영을 나눈다", the "목표 구조" tag, the flat Japanese explanatory-manual style (confident charcoal outlines, sky blue, restrained pale yellow, white background), the author character, the Git badge, the single blue arrow "검사 후 설치", the knowledge_root panel with all its labels, and the bottom row of five equal panels with their illustrations and order. Landscape 3:2, 1536x1024.

Make ONLY these text changes:
1. LEFT panel: the fourth folder card label "기본 지시·권한" becomes "행동 원칙·권한". The other three cards stay "코드", "지식·실무서", "전문가 구성".
2. MIDDLE panel header "설치 판본" becomes "설치 버전". Its first label "검사한 프로그램 · 구성" becomes "프로그램 · 구성 · 도구 · 모델". Keep "install_root" and "업무 계정은 읽기만".
3. test_root panel: add a short middle label above the bottom band, in the same position and size as the middle labels of the other bottom panels: "시험 DB · 파일 · 모의 시스템". The bottom band becomes a person icon plus "시험 계정", styled exactly like "평가 계정" and "관리 계정".
4. evaluation_root middle label "보호 시험 · 정답" becomes "보호 시험 · 정답 · 공격 시험". Keep "평가 계정".
5. control_root: replace the two middle lines with exactly two lines: "삭제·사용 중지 기록" and "업데이트 신뢰 · 감사 확인점". Keep "관리 계정".
6. backup_target middle label "DB · 파일 · 보호 이력" becomes "DB · WAL · 파일 백업". Keep "PC 밖 · 덮어쓰기 방지".
7. 비밀 저장소 panel unchanged.
No new title, subtitle, footer or paragraph. Every Korean word spelled exactly as given; English paths verbatim lowercase with underscores and the trailing slash on "expert-factory/". All labels at least as large as now, none cut off or touching panel edges, no overlapping text.
```

### knowledge-root

- 적용 파일: `docs/images/file-folder-structure/knowledge-root.png`
- 채택 원본: `/Users/haris/.codex/generated_images/file-folder-structure-2026-10-23c/knowledge-v1.png`
- 고친 곳: `scopes/<scope-id>/` 안 폴더를 넷에서 여섯으로 늘려 `models/`("범위 전용 모델")와 `releases/`("고객 전용 배포물")를 더했다. 3×2 격자로 배치하고 아래 두 띠를 조금 내렸다.

```text
Edit the attached Korean illustrated folder tree "운영 자료는 이렇게 보관한다". Preserve the title, the knowledge_root parent folder, the style (charcoal outlines, sky-blue folders, pale yellow restricted folders, white background), the LEFT "공통 자료" group and the MIDDLE "이용이 제한된 자료" group with all their labels, the "여러 고객에 걸친 것" band with its two folders and labels, the bottom "같은 저장소의 관리 폴더" shelf with its five folders and labels, and both outer connecting lines (left to the shelf, right to the band). Landscape 3:2, 1536x1024.

Make ONLY this change, in the RIGHT group "고객 업무" (tenants/<tenant-id>/):
The scopes/<scope-id>/ compartment (pill "열람 범위별") now holds SIX inner folders instead of four, arranged as a neat grid of 3 columns x 2 rows, all inside the scopes compartment:
 Row 1: "objects/<key-id>/" label "키별 원본·확정"; "derived/" label "가공 자료"; "exports/" label "내보낸 사본".
 Row 2: NEW "models/" label "범위 전용 모델"; NEW "releases/" label "고객 전용 배포물"; "cases/" label "업무별 폴더".
Keep the browser-profiles/ compartment above it with label "고객 계정 로그인 · 백업 제외" and its lock. To make vertical room, make the RIGHT group taller and shift the "여러 고객에 걸친 것" band and the bottom shelf slightly down and make them a little more compact; the LEFT and MIDDLE groups may stay their current height. Text in the six folders must be as large as the labels in the LEFT "공통 자료" group and readable when the image is shown 1100px wide. "objects/<key-id>/" must fit on one line inside its folder card.
All technical paths verbatim and case-sensitive, including hyphens, underscores, slashes and angle brackets. No new paragraph, subtitle or footer. No text cut off, overlapping or touching borders. Lines must not pass through any frame or label.
```

### case-folders

- 적용 파일: `docs/images/file-folder-structure/case-folders.png`
- 1차 편집 원본(`review-sheet/` 글자 작음, 미채택): `/Users/haris/.codex/generated_images/file-folder-structure-2026-10-23c/case-v1.png`
- 채택 원본: `/Users/haris/.codex/generated_images/file-folder-structure-2026-10-23c/case-v2.png`
- 고친 곳: DB 목록 "판본" → "버전". `deliveries/`에 `review-sheet/`("검토표 · 맡긴 사람만")를 `package.zip` 옆 별도 폴더로 더했다.

```text
Edit the attached Korean illustration "업무 한 건의 폴더를 열어 보면". Preserve everything — layout, drawing style, colors, the scopes/<scope-id>/ enclosure, objects/<key-id>/, the cases/<case-id>/ folder, the snapshots/, sessions/, traces/ and work/ columns with all their text, the bottom process strip "결과를 확정할 때" with all its text and arrows — EXCEPT these two changes:
1. The DB note at top right lists "권한 · 계획 · 상태 · 판본". Change the fourth bullet "판본" to "버전". Keep "DB" and "현재 상태의 기준".
2. The rightmost column "deliveries/" (heading "납품 묶음") now shows THREE items stacked vertically, compact enough to fit inside the column without touching borders: checklist "manifest.json"; parcel "package.zip"; and NEW a small folder "review-sheet/" with a small lock and label "검토표 · 맡긴 사람만". The review-sheet folder sits beside the parcel, not inside it (it is never inside package.zip). Shrink the checklist and parcel icons to make room.
No other changes. Text verbatim, slashes, hyphens and angle brackets exact, nothing cut off, overlapping or touching borders. No new paragraph or footer.
```

2차 편집(1차 편집 원본 입력):

```text
Edit the attached Korean illustration. Keep every element, word, path, line, color and position exactly the same, EXCEPT improve legibility in the rightmost "deliveries/" column:
The small folder text "review-sheet/" is too small. Make "review-sheet/" the same text size as "package.zip", on one line inside its folder card without touching edges, with the small lock to its left. Keep the label below it "검토표 · 맡긴 사람만" at the same size as "package.zip". To make room, make the checklist and parcel icons slightly smaller and move them up a little; keep "manifest.json" and "package.zip" text unchanged and readable. Everything must stay inside the deliveries/ column with a small margin above its bottom border. No other changes, no new text.
```

세 장 모두 1536×1024px PNG다. 원본 크기와 1100px 폭 headless Chromium 표시를 직접 열어 한글·경로 글자, 포함 관계, 선 경로, 잘림·겹침을 확인했다.

## 2026-10-23 — 14절 전면 갱신·신규 제작

현재 본문을 기준으로 기존 3장을 편집하고 그림이 없던 11개 절에 신규 그림을 만들었다. 내장 `image_gen`만 사용했다. 모두 1536×1024 RGB PNG이며 생성 원본을 바이트 변경 없이 프로젝트에 복사했다. 신규 그림은 기존 그림의 하늘색·연노랑·짙은 윤곽선을 문장으로 지정했다. 외부 제작 에셋은 쓰지 않았다.

그림 속 경로는 읽기 쉽도록 일부 ID 단계를 생략한다. 정확한 전체 경로·예외·권한은 본문을 따른다. 1절 번호는 요약 그림의 순서이고, 10절 버전 번호는 예시다.

### 1절 — judgment-input

- 적용: `judgment-input.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-e272e1b3-8e58-4edb-a670-f9698f8d0b81.png`
- 확인: 원본→판단용 본문→색인·검증된 관계→검색→관리 프로그램→판단 입력→주 모델→검증. 온톨로지 정의를 DB 내부에 넣은 초안을 수정해 OWL·SHACL 검사와 검증된 관계를 구분.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "자료가 판단 입력이 되기까지". Show an orderly two-row pipeline, four large illustrated stations per row. Top row flows LEFT to RIGHT: "접수" with sealed folder "objects/"; "판독·보호 처리" scanner, privacy shield and folder "derived/"; "색인·관계" one database containing small "BM25", "벡터", "온톨로지" labels and a tiny network; "검색" magnifier with "하이브리드 · GraphRAG". From this final station draw down along the right edge, to bottom row flowing RIGHT to LEFT: "관리 프로그램" sorting a pack labelled "업무 상태 + 검색 결과"; "판단 입력" organized four-tab pack whose tabs read "업무 식별", "목표·조건", "필수 근거", "보충 자료", folder caption "snapshots/"; "주 모델" professional at screen interpreting the packet; "검증·확정" check document beside folder "objects/". Number stations 1 to 8 in small circles matching that route. Place a small lock and short label "전달 직전 권한 재검사" on the arrow immediately before 주 모델. The model receives only the packet, no original-folder bypass arrow. Under the indexing station small exact label "PostgreSQL". Under verification "원본 대조 · 독립 재판단". Do not imply ontology validation proves factual truth.
```

- 초안 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-dec44073-f2a9-4c9f-ab4a-dd6ad17721d0.png`

수정 지시:

```text
Edit only station 3 of this Korean diagram. Preserve every other element, exact text, arrows and layout, 1536x1024. Inside the PostgreSQL cylinder, replace the bottom label "온톨로지" with "검증된 관계". The ontology definition is an authored file, not stored inside this cylinder. Add a small separate checklist sheet above or beside the network outside the cylinder labelled "OWL·SHACL 검사" without crossing the neighboring station. Keep "BM25", "벡터", "PostgreSQL" unchanged. Do not change numbers or any other panel.
```

### 2절 — storage-locations

- 적용: `storage-locations.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-72443666-db61-454f-ac33-05211016f4bb.png`
- 확인: test/evaluation/control과 PC 밖 WORM 백업, 비밀 저장소, 업무 건 키의 예약 삭제 저장소를 분리. 업무 실행의 install_root 읽기 전용 유지.

```text
Edit this Korean architecture illustration. Keep 1536x1024 landscape, title "작성·설치·운영을 나눈다", top three columns expert-factory/, install_root, knowledge_root, and the inspection arrow from authoring to installation. Match existing friendly outlined blue/yellow illustrations on white. The lower part must clearly separate the new backup/key boundaries; redesign lower 42% into TWO horizontal rows of compact illustrated cells, three per row. First row: (1) "test_root", computer and DB, short label "시험 전용 DB·파일"; (2) "evaluation_root", locked exam cabinet, label "보호 시험·정답"; (3) "control_root", signed ledger, label "삭제·철회·신뢰 기록", second line "PC 밖 별도 보관". Second row: (4) "backup_target", remote locked storage (not a locally plugged disk), label "DB·파일 백업", second line "PC 밖 · WORM"; (5) "비밀 저장소", local safe, label "키·토큰·인증정보", second line "업무 건 키는 백업 제외"; (6) "업무 건 키 사본", remote key vault, label "PC 밖 예약 삭제 저장소", second line "파일 백업과 분리". Do not draw arrows linking all six cells; these are separate boundaries. Keep top three column contents and styles, but simplify vertical spacing to fit two rows with readable large Korean text. No decorative footer.
```

### 3절 — knowledge-root

- 적용: `knowledge-root.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-b9e2327d-f94f-4f85-a241-907476c4ffe8.png`
- 확인: 고객 범위의 models·releases 추가, browser-profiles와 scopes 형제 관계, 공동 범위·사무소 계정·관리 폴더 루트 소속, 제한 자료의 저장 허용 조건 확인.

```text
Edit this existing Korean folder-tree illustration for the current architecture. Preserve style, title, knowledge_root root, exact hierarchy, and management shelf (config/, staging/<scope-id>/, cache/<scope-id>/, stores/postgres/, operations/). Canvas 1536x1024 landscape. Redesign the RIGHT "고객 업무" group to show SIX small folders in a readable 3 columns by 2 rows inside scopes/<scope-id>/: "objects/<key-id>/" caption "키별 원본·확정"; "derived/" caption "판단용 본문"; "exports/" caption "내보낸 사본"; "models/" caption "고객 전용 모델"; "releases/" caption "고객 전용 배포"; "cases/" caption "업무별 폴더". browser-profiles/ stays a SIBLING of scopes/, inside tenants/<tenant-id>/, caption "고객 로그인 · 백업 제외". Give this right group half the width, narrow shared and restricted groups slightly with readable labels. Keep shared/collections/<collection-id>/ and restricted/<scope-id>/collections/<collection-id>/ with objects/, derived/, exports/; change their derived caption from "가공 자료" to "판단용 본문". For restricted add brief label "저장 허용 자료만". Keep joint-scopes/<scope-id>/ and offices/<office-id>/browser-profiles/ as DIRECT CHILDREN of knowledge_root, with the external connection not crossing text. No duplicate folders. Preserve all angle brackets and hyphens exactly. Do not add paragraphs.
```

### 4절 — knowledge-authoring

- 적용: `knowledge-authoring.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-7c656237-9d80-403f-86f9-10d6d1d35bc9.png`
- 확인: 공통·법률·분야 작성 원본, 전문가 knowledge.lock 참조, 구조 검사와 원문·업무 검증 구분, 고객 전용 배포물 분리.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "분야 지식과 전문가를 연결한다". Main composition is a knowledge library linked to TWO professional portfolios, not a long list. Left half: an open blue cabinet titled "expert-factory/" with three shelves labelled "공통 개념", "법률 개념", "분야 지식". Paths respectively "knowledge/core/ontology/", "knowledge/collections/legal-kr/ontology/", "knowledge/domains/<domain-id>/". In the last shelf show three illustrated books "온톨로지", "실무서", "스타일·사례". On the right show two equally sized blue portfolios "세무사" and "회계사", each containing one card "knowledge.lock". Clean lines from the single 분야 지식 shelf to both portfolios labelled "ID·버전 참조" once, clearly shared reference, not copies. Below a horizontal validation path: illustrated ontology checklist "구조 검사" then separate evidence magnifier "원문 검토·업무 시험" then installed package "검사한 버전 설치". In a separate yellow locked enclosure at bottom right draw "고객 전용" folder "scopes/<scope-id>/releases/" with caption "공용 배포물과 분리". No arrows from the private enclosure to the public library.
```

### 5절 — database-file-roles

- 적용: `database-file-roles.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-de413b8f-253e-4846-aec1-9c4d888afa58.png`
- 확인: 상태·권한·지식·검사 DB 기록과 본문 파일의 ID·버전·해시 연결. control_root 별도 표시.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "현재 상태는 DB, 본문은 파일". Three visual zones. LEFT 35%: one large PostgreSQL cylinder with four compact record cards "상태·계획", "권한·보존", "지식·관계", "근거·검사". CENTER 20%: a single connecting bridge with linked tag icons labelled "ID · 버전 · 해시". RIGHT 45%: one file cabinet with six illustrated drawers in 2 columns by 3 rows: "objects/" with "원본·확정 파일"; "derived/" with "판단용 본문"; "snapshots/" with "고정한 판단 입력"; "sessions/" with "지속 대화"; "traces/" with "보호 실행 기록"; "exports/" with "고정 사본". Bottom left show small manager with a control panel "관리 프로그램", arrow to DB "검증된 함수로 변경". Bottom right separately show a locked record ledger "control_root" caption "삭제·사용 중지 기록". Do not draw current state JSON files or imply that exports overwrite the database. Leave all text large and succinct.
```

### 6절 — ingest-versioning

- 적용: `ingest-versioning.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-b326452c-3c3d-4e77-82bd-46f37215f6a9.png`
- 확인: staging→검사→암호화 새 쓰기→fsync·해시→DB 등록·색인 예약→접수 사본 정리. source_version_id·recipe_id·result_id 분리.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "받은 파일을 원본으로 확정한다". Six numbered illustrated steps in a 3-column by 2-row serpentine sequence. Top left 1 "받는 중 등록", intake tray labelled "staging/"; top middle 2 "형식·출처·해시 검사", person with magnifier; top right 3 "암호화해 새로 쓰기", locked folder labelled over two lines "objects/<key-id>/" and "sha256/". Down arrow to bottom RIGHT 4 "기록 완료·해시 확인", disk and check, short code "fsync"; left to bottom middle 5 "DB 등록·색인 예약", one database with small label "한 트랜잭션"; left to bottom left 6 "접수 사본 정리", empty staging tray with check. In a separate footer-width inset visually distinct from the sequence, show an ORIGINAL document "source_version_id" linking to a recipe gear "recipe_id" then two sibling outputs "result_id A" and "result_id B"; small label "확정 결과는 새 버전으로". This is about new immutable results, never overwrite. No deletion symbol on original objects, only on staging copy. Do not imply hash proves provenance.
```

### 7절 — change-propagation

- 적용: `change-propagation.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-b54a0b5c-0d9e-40c3-8915-df67453c91f3.png`
- 확인: 즉시 사용 보류, 의존 관계 추적, 진행 중·기납품 영향 구분, 과거 버전 보존, 발송과 수신 상태 구분.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "근거가 바뀌면 쓴 곳까지 찾는다". Top horizontal visual chain of six stations with clean right-pointing arrows: "원문·기준" (document new version), "추출·색인·관계" (database plus network), "판단 입력" (organized packet), "판단·계산" (person and calculator), "결과물" (report), "전달처" (recipient). Label the chain once "의존 관계". Near first node a yellow pause shield "변경 접수 즉시 사용 보류". Middle row a magnifier from the chain to TWO separated destinations: "진행 중인 업무" with revised report icon, caption "다시 검토"; "이미 낸 결과" with recipient icon, caption "영향 판단 후 정정". Bottom show correction states on four connected paper cards "승인 대기" → "발송 대기" → "발송 완료" → "수신 확인", with a separate small yellow branch "실패·확인 불가". Small locked archive at bottom left "과거 버전 보존". Never show the four correction states as all automatically completed. No time, efficacy or legal claims beyond listed words.
```

### 8절 — case-folders

- 적용: `case-folders.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-322fac40-d7ba-4136-92f5-69b7f032d160.png`
- 확인: snapshots 판단 입력 추가, SDK 로그는 traces·도구 로그는 logs, review-sheet는 deliveries 안이며 package.zip 밖. 범위의 objects와 cases 형제 관계 유지.

```text
Edit this existing Korean illustrated folder diagram. Retain the charcoal outlines, sky blue and pale yellow palette, white background, folder hierarchy, 1536x1024 landscape canvas and all other wording. Fix three inaccurate areas: 1. Within work/ the logs/ caption currently says "도구·SDK 출력"; replace it with ONLY "도구 출력". 2. Within traces/ replace the central two lines with three readable short lines "모델 입력·응답", "도구 호출·결과", "SDK 출력 로그". Keep "관리 프로그램만 기록". 3. Within snapshots/ change the small yellow label "실행 기준" to "판단 입력·실행 기준" and bottom label to "고정한 계획·판단 입력·환경". Keep the five case subfolders and objects/<key-id>/ as the sibling of cases/<case-id>/ in the same scope. In deliveries/ add a small separate slim document labelled "review-sheet/" with "내부 검토표", visibly beside the package.zip box and not inside it; fit by slightly reducing package icon. No other changes; no extra title or footer.
```

### 9절 — evaluation-delivery

- 적용: `evaluation-delivery.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-e5c1d32b-9563-4d19-ae35-5575926b6e25.png`
- 확인: 정답 보호, 허용 입력→격리 실행→평가 계정 결과 회수, 외부 실제 발송 차단. review-sheet는 deliveries 안이며 package.zip과 별도. 채점이 차단 대상으로 보이던 초안 수정.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "시험 결과와 납품을 나눈다". Two big clearly separated lanes. TOP lane "시험": left locked cabinet "evaluation_root" containing "정답·채점 자료", caption "평가 계정만"; middle a fenced laboratory labelled "test_root" with three sequential subfolders "inbox/" → "runs/ · mocks/" → "outbox/". Show ONLY allowed-input envelope from evaluator to inbox labelled "허용 입력", and output envelope from outbox back along bottom edge to evaluator labelled "결과 회수". A red crossed outbound arrow at boundary with short label "실제 발송 차단". Outside laboratory to right show no package, only checklist "채점". BOTTOM lane "납품": independently from left "확정 결과" report → "권한·내용 검사" person with magnifier → "백업 도착 확인" remote safe → "deliveries/" containing package "package.zip" and file "manifest.json". Beside but not inside the package show separate locked sheet "review-sheet/" label "내부 검토표". Small crossed arrow between upper lane and lower lane with text "시험 결과는 납품 제외". Keep these two lanes independent; absolutely no implication the protected answers reach the tested agent.
```

- 초안 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-57e1e974-4086-43d5-b5f4-7e66ecaceda2.png`

수정 지시:

```text
Edit this illustration to fix exactly two relationship errors, preserving all other content, style, dimensions, Korean labels and layout. 1. The red blocked outbound arrow in the upper test lane must lead to an EXTERNAL SYSTEM, not grading. Replace the far-right clipboard currently labelled "채점" with a simple external server icon labelled "외부 시스템"; retain "실제 발송 차단". Add a small grading clipboard beside the evaluator at far LEFT labelled "채점", so the yellow "결과 회수" arrow clearly leads to that evaluator. No answer material may flow to test_root. 2. In the lower lane, review-sheet/ is physically INSIDE deliveries/ but separate from package.zip. Widen the blue deliveries/ parent folder boundary to enclose package.zip, manifest.json AND review-sheet/. Keep review-sheet/ visually in a separate internal compartment with a vertical divider, with "내부 검토표". Do not imply review-sheet/ is included in package.zip. Nothing else changes.
```

### 10절 — installation-updates

- 적용: `installation-updates.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-eb089967-80ff-4323-b9df-4cf931f9b397.png`
- 확인: 프로그램·공용 지식·전문가·도구·부품 분리, 검사 후 인계·전환, DBOS 프로세스 하나와 옛 부품 보존. v1.2.0/v1.3.0은 설명용 가상 버전.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "새 버전을 검사하고 전환한다". Left 40% one organized installation cabinet "install_root" with FIVE visible drawers: "applications/", "knowledge/", "experts/", "tools/", "components/". Show small tags "프로그램", "공용 지식", "전문가", "도구", "고정 부품" matching drawers. On experts drawer attach small readable cards "allowed-scope.json" and "knowledge.lock". Right 60% a before/after visual: old installed machine "현재 버전" alongside boxed candidate "새 버전". Under candidate three small checks "서명", "호환", "시험". Then a clear three-step pathway "옆에 설치" → "진행 업무 인계" → "실행 버전 전환". At end one active process icon labelled "DBOS 실행 1개"; old machine is archived with label "옛 부품 보존", not running. Bottom show two separate rewind controls "프로그램 되돌리기" and "DB 되돌리기" and one small protected ledger "변경·거래 기록 보존". No arrow that erases history, no running two versions simultaneously.
```

### 11절 — storage-recovery

- 적용: `storage-recovery.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-f8f4ef24-bbdc-41ad-910a-16e1fd41c1e3.png`
- 확인: 70·85·95% 초기 제안값, 삭제 차단·의존 사본·보존 분리·키 폐기, 최신 삭제 기록부터 격리 복원·권한 재적용 후 재개. 5분/1시간을 달성값 아닌 목표로 표시.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "지우고 복원해도 제한을 지킨다". Three clean horizontal illustrated lanes, each using a distinct physical scene but consistent blue/yellow palette. Top short lane "용량" with disk gauge and three increasing marks: "70% 경고", "85% 비필수 수집 보류", "95% 새 대량 입력 중지"; small qualifier "초기 제안값". Middle lane "삭제": shield "조회·재사용 차단" → magnifier following linked files "연결된 사본 찾기" → locked archive "보존할 자료 분리" → disappearing key and file stack "키·사본 폐기 확인". Keep originals until dependent copies identified, no instant-delete success. Bottom lane "복원": remote protected ledger "최신 삭제 기록" → isolated PC restoring database and files "격리 복원" → shield/check "차단·권한 재적용" → machine starting "업무 재개". Add a modest target badge with exact short two-line text "복구 목표" / "손실 5분 · 재개 1시간"; do not show it as achieved. In lower restore lane make the final arrow visibly pass through the shield before reaching service. No dense paragraphs or unnecessary decorative boxes.
```

### 12절 — current-target

- 적용: `current-target.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-a1e97983-5254-43c8-8493-82c882e661c2.png`
- 확인: 기존 부품과 미구현 보호 장치를 본문 현황 기준으로 구분, 검색 변경은 전환 전후 시험 대상으로 표시.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "기존 부품과 새로 만들 부분". Visual workshop comparison, left titled "현재 부품" and right titled "새로 구현". Left a sturdy blue toolkit containing three clearly illustrated groups: folder and database "원본 저장·버전·재개"; search magnifier "BM25 · Kiwi · KURE-v1"; linked vocabulary books "OWL · SHACL". Lower left label "data/objects/ · data/postgres/". Center a person inspecting an inventory clipboard labelled "목록·권한·용량 확인", arrow from current parts through inventory to target workshop. Right show THREE unassembled outlined modules with blueprint markings (not green checkmarks): shield+key "범위 격리·암호화"; laboratory+orchestrator "Podman · DBOS"; remote vault+restore loop "WAL · 백업·복구". Under right an outlined search module "pg_textsearch · Qwen3" with caption "전환 전후 시험". One small header qualifier under title is allowed only as a tiny tag "본문의 현황 기준". Do not pretend these new protections have been implemented or migration completed. Preserve existing IDs visually with a tagged part carried from left to right labelled "기존 ID 유지".
```

### 13절 — migration-sequence

- 적용: `migration-sequence.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-9ca6a0c4-1494-40a6-8b15-68f03207e458.png`
- 확인: 7단계 순서, 합성·공개 자료부터 시작, 범위별 ID 유지와 참조 없는 사본 정리. 실고객 관문의 체크박스 중립화 및 잘못된 1단계 선행 화살표 제거.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "한 범위씩 확인하며 옮긴다". A seven-stop illustrated migration route. Top row four stops left to right: 1 "현황 목록" clipboard and files; 2 "한 자료실·한 업무" one folder and workstation; 3 "권한·복구 검증" lock and restore arrows; 4 "지식·구성 배포" books and package. Route goes down at far right then bottom row RIGHT to LEFT: 5 "납품·운영" inspected delivery box; 6 "범위별 이관" copying one locked folder between disks with short label "ID 유지"; 7 "이관 뒤 정리" magnifier checking old-copy tags before bin with label "참조 없는 사본만". Every arrow clearly directional, no crisscross. Between the rows at left show a separate yellow gate with human checklist "첫 실고객 관문", beneath it ONLY short labels "허용 업무", "충돌 검사", "암호화·격리", "백업·삭제 검증", "계약·동의". This gate is a prerequisite shown as closed, not all green checks. Small tag at step 2 "합성·공개 자료부터". Do not use a big completed check for unfinished architecture. No implication all current data will be moved now.
```

- 초안 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-acacdef4-f630-4b7d-ab00-b0b5c23c8b2f.png`

수정 지시:

```text
Edit only the small lower-left "첫 실고객 관문" inset of this illustration. Keep all seven numbered steps, route arrows, drawings, text, colors and positions exactly as they are. Remove the grey dashed arrow that currently points upward from the first-customer gate to step 1 현황 목록; the gate must be an independent callout, not a prerequisite to making an inventory. In the five gate list rows replace every status icon, including green checked box and red exclamation icons, with identical EMPTY outlined square checkboxes. This is an unassessed checklist, not a current pass/fail report. Preserve labels "허용 업무", "충돌 검사", "암호화·격리", "백업·삭제 검증", "계약·동의". Keep the lock on the gate. No other changes.
```

### 14절 — material-storage-map

- 적용: `material-storage-map.png`
- 채택 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-7b2157e0-4427-4a82-8f2e-f555239bfd8d.png`
- 확인: 재료별 폴더 아닌 공동 저장 자리, PostgreSQL·범위 파일·install_root의 세 실선과 보호 시험·관리 기능 요청 점선을 정확한 대상에 연결.

```text
Create one polished Korean educational illustration for a technical architecture document. Landscape 1536x1024, opaque clean white background. Consistent Japanese explanatory editorial illustration style: bold smooth dark charcoal outlines, sky-blue folders and machines, soft yellow emphasis, small green checks for verified states, subtle hand-drawn dimensional shading. Warm simple professional human illustrations only where useful. Large crisp Korean sans-serif labels and exact technical identifiers. Visual objects and structural relationships dominate; no paragraphs, no subtitle, no filler footer, no watermark. Generous safe margins. Arrows must be unambiguous and never cross text. Use only the listed text.
Title "79개 재료는 저장 자리를 함께 쓴다". Left a simple fan of many small numbered document tabs inside a large open reference book labelled "79개 재료"; do not render 79 legible tiny labels, just a suggestive fan and clear 79. Center a professional at a management console labelled "관리 프로그램". Lines from book to console then fan out without crossing to FOUR large destination groups occupying right 65% in 2x2 layout: (top left) one blue DB cylinder "PostgreSQL" with short label "상태·권한·지식·검사"; (top right) nested locked blue folders "범위별 파일" with three short rows "objects/ · derived/", "snapshots/ · sessions/ · traces/", "work/ · deliveries/"; (bottom left) installed book/package cabinet "install_root" with label "프로그램·지식·전문가·도구"; (bottom right) TWO separate locked folders "evaluation_root" and "control_root" with caption "보호 시험 · 관리 기록". The bottom-right line from manager must be dashed and labelled "관리 기능에 요청", indicating the business executor cannot directly read them. No folder per material, no falsely exclusive numerical range-to-storage mapping. No decorative footer.
```

- 초안 원본: `/Users/haris/.codex/generated_images/01a16737-a0f3-7ff0-9b0d-a02bb325693e/exec-c24a4a60-398e-4f25-b331-94a20e114962.png`

수정 지시:

```text
Edit the right half of this Korean illustration to correct the connector destinations. Preserve title, book "79개 재료", and management console. Replace the four destination panels currently in a 2x2 grid with FOUR WIDE HORIZONTAL ROWS stacked vertically at the right, all with the SAME left boundary. Each row receives exactly ONE separate arrow from the management console, no arrow crossing another and none entering the wrong row. Row 1: blue cylinder "PostgreSQL", caption "상태·권한·지식·검사". Row 2: locked folders "범위별 파일", two lines "objects/ · derived/ · snapshots/" and "sessions/ · traces/ · work/ · deliveries/". Row 3: installation cabinet "install_root", caption "프로그램·지식·전문가·도구", SOLID blue arrow. Row 4: two locked folders "evaluation_root" and "control_root", caption "보호 시험 · 관리 기록", DASHED yellow arrow labelled "관리 기능에 요청". Enlarge right area and shrink the book slightly to fit. All four arrowheads end at their corresponding row's LEFT boundary. No extra arrows, no duplicated numbers on book tabs; use tiny plain unlabeled tabs with only the cover reading 79개 재료. Keep canvas 1536x1024, same style, large legible type.
```
