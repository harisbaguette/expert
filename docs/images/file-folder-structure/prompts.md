# 파일·폴더 구조 일러스트 제작 기록

현재 사용본은 **2026-10-23 수정본**이다. 현재 본문과의 대조, 수정 프롬프트와 생성 원본은 아래 [2026-10-23 갱신](#2026-10-23-갱신)에 기록했다. 앞의 2026-10-22 기록은 최초 제작 이력이다.

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
