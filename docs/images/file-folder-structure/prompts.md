# 파일·폴더 구조 일러스트 제작 기록

현재 사용본은 **2026-10-23 2차 수정본**이다. 현재 본문과의 대조, 수정 프롬프트와 생성 원본은 아래 [2026-10-23 2차 갱신](#2026-10-23-2차-갱신)에 기록했다. 그 앞의 [2026-10-23 갱신](#2026-10-23-갱신)은 1차 수정 이력이다. 앞의 2026-10-22 기록은 최초 제작 이력이다.

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
