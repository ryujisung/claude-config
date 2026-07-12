---
name: jira-write
description: >-
  Jira(SOMA) 작성 두 가지가 메인 — ① 티켓(작업·에픽) 제작/수정 ② 티켓 댓글(진행·결정·결과·질문) 작성.
  신 포맷(결론 먼저·짧게·약어 금지)으로 빈 카드·티켓 과쪼갬·맥락 없는 댓글을 막는다. "Jira/SOMA에 티켓·작업·에픽
  만들어/수정", "이 이슈에 댓글/코멘트/진행 남겨"처럼 대상이 Jira일 때만 발동. 발동 안 함: Confluence 문서(=doc-publish),
  soma 로컬 문서(founder/·ops/·inbox/), 코드 작성, 단순 대화.
---

# jira-write — Jira 작성 (티켓 + 댓글)

Jira `SOMA`가 **실행의 정본(SSOT)**. 이 스킬의 두 메인:
- **A. 티켓 제작/수정** — 작업·에픽을 신 포맷 카드로.
- **B. 댓글 작성** — 진행·결정·결과·질문을 결론 먼저로 해당 티켓에.

공통 톤: **결론 먼저 · 짧게 · 약어 풀어쓰기.** (doc-publish의 Jira 짝)

> **발동 범위**: 대상이 **Jira(SOMA)**일 때만. Confluence 문서는 `doc-publish`, 코드·로컬문서·대화는 대상 아님. 애매하면 "Jira에 쓰는 거 맞아? (티켓/댓글)" 1줄 확인.

## 공통 고정값 (MCP — Atlassian Rovo는 deferred → 먼저 `ToolSearch`)
`ToolSearch("select:createJiraIssue,editJiraIssue,addCommentToJiraIssue,getJiraIssue,getTransitionsForJiraIssue")`
- cloudId = `205faf1b-4810-4ed3-843d-410a3a6dcc9b`, projectKey = `SOMA`.
- description·commentBody는 **항상 `contentFormat:"markdown"` 명시**(기본값이 도구마다 달라 생략 금지).

## 공통 불변식 (어기면 작성 중단)
1. **결론 먼저** — 티켓은 첫 줄 `【결과】`, 댓글은 첫 줄 `【태그】 + 한 줄 요지`.
2. **빈 내용 금지** — 본문 없는 티켓·댓글 금지.
3. **쉬운 말 · 약어·코드 격리** — 본문은 **쉬운 일상어**로 쓴다(영어 약어·내부용어 빼고, 꼭 필요한 도구명만 괄호로 1회 풀기 — 예 "GitHub(코드 저장소)"). PM이 카드를 제일 많이 읽는다. 코드·변수·경로·브랜치는 `참고(개발용):` 한 줄로만.
4. **할 일은 카드로** — 새로 생긴 추적할 일은 댓글·본문에 방치 말고 작업 카드로(또는 상위 완료조건에).
5. **Confluence는 클릭 링크로** — 티켓·댓글에서 Confluence 문서를 가리킬 땐 평문 page ID(숫자)만 적지 말고 **무조건 마크다운 링크**로: `[제목 또는 pageID](https://hiws99.atlassian.net/wiki/spaces/TSSNN/pages/<pageId>)`. (Jira 이슈 키 `SOMA-NN`은 자동 링크되니 평문 OK.)

---

## A. 티켓 제작/수정

### 단위 — 잘게 쪼개지 말고 묶는다
- **작업 1개 = 한 사람이 이어서 하는 한 덩어리**(기본 3시간~반나절).
- 3시간 미만 잔작업 → 독립 티켓 만들지 말고 **상위 작업의 완료조건 체크리스트로 흡수.**
- 한 사람·한 영역의 연속 작업은 단계가 여럿이어도 **1티켓**(단계=완료조건). 명세·설계는 **산출물 1개 = 티켓 1개.**
- **티켓 양산 금지(특히 AI).** 만들기 전 자문: "한 사람이 이어서 하는 독립 단위이고 3시간 이상인가? 아니면 기존 완료조건으로?"
- 계층 = **에픽 > 작업 2단계.** 스토리·하위작업 미사용.

### 양식
- **제목 = 동사 + 대상** (예 "API 명세 작성"). 제목에 `[태그]` 금지(분류는 에픽으로).
- description 템플릿:
```
【결과】 (끝나면) 사용자/시스템이 ___ 하게 된다.

## 왜  (2줄 이내, 처음 쓰는 약어는 괄호로 풀기)
무슨 문제라서 하는가.

## 완료 조건  (예/아니오로 판정되는 것만, 3~6개, 사용자·동작 기준)
- [ ] 사용자가 보는 변화 / 동작 기준으로

## 검증 지표  (검증 주 대상 작업이면 필수)
- 무엇을 측정해 성패를 가르나 (지표 + 목표치)

## 참고
- 정본 문서 링크 (Confluence는 `[제목](https://hiws99.atlassian.net/wiki/spaces/TSSNN/pages/<id>)` 마크다운 링크로 · 이슈는 SOMA-NN)
- 참고(개발용): 건드리는 코드·변수·브랜치
```
- 완료조건(AC) = **Specific · Testable · Clear.** **DoD(모든 카드 공통)**: AC 충족 + (코드면)PR 리뷰·동작 확인 + 관련 문서 갱신 + (검증주면)지표 기록.

### 절차
1. **입력 확정**: 무엇을 · 소속 에픽(키) · 우선순위(Highest~Low) · 담당자 · 검증주 여부 · 새/수정. 불명확하면 1개만 되묻는다.
2. **입도 점검**: 3시간 미만이거나 기존 작업의 연속이면 → 독립 티켓 대신 **기존 카드 완료조건 흡수**를 제안하고 멈춘다.
3. **작성**: 제목(동사+대상) + 템플릿.
4. **발행**:
   - 새 작업: `createJiraIssue(cloudId, projectKey="SOMA", issueTypeName="작업", summary, description, contentFormat="markdown")`
   - issueTypeName = `작업`(Task) / `에픽`(Epic) / `버그`(Bug). **`스토리`·`하위 작업` 금지.**
   - 에픽 소속: `additional_fields:{"parent":{"key":"SOMA-NN"}}` (team-managed는 parent가 에픽 링크).
   - 우선순위·라벨: `additional_fields:{"priority":{"name":"High"}, "labels":[...]}`. 담당자: `assignee_account_id`.
   - 수정: `editJiraIssue(cloudId, issueIdOrKey, fields={...}, contentFormat="markdown")`.
5. **보고**: 이슈키 · URL · 한 줄 요약.

---

## B. 댓글 작성

### 언제
진행 업데이트 · 결정/변경 기록 · 검증/리뷰 결과 · 막힌 점/질문. (스탠드업·리뷰·검증에서 나온 맥락을 **그 티켓에** 남긴다.)

### 양식 — 첫 줄 `【태그】 한 줄 요지`, 그 아래 짧게
태그: `【업데이트】` 진행 · `【결정】` 결정·변경 · `【결과】` 검증·리뷰 · `【질문】` 막힌 점·요청
- **【업데이트】**: 한 일 · 다음 · 막힌 점
- **【결정】**: 무엇을 · 왜 (큰 결정이면 Confluence `[결정]` 문서로 만들고 댓글엔 링크)
- **【결과】**: 관찰 → 결론 → 액션(→ 새 카드)
- **【질문】**: 막힌 점 · 필요한 것 · @담당

원칙: 약어 풀기 · 코드는 `참고(개발용)`로 · 새 할 일은 카드로(공통 불변식 4).

예:
```
【업데이트】 /coach GA4 퍼널 dev 확인 완료, prod 배포만 남음.
- 한 일: 6단계 이벤트 + 단계별 error 발화를 GA debugview로 확인.
- 다음: prod 배포 후 측정ID 일치 확인.
- 막힌 점: Vercel 업로드 한도 → 우회 검토 중.
```

### 절차
1. **대상 이슈키 확인** (없으면 1줄 되묻기).
2. (필요시) `getJiraIssue(cloudId, issueIdOrKey)`로 현재 상태 파악.
3. 태그 + 요지로 댓글 작성(짧게).
4. **발행**: `addCommentToJiraIssue(cloudId, issueIdOrKey, commentBody, contentFormat="markdown")`. 기존 댓글 수정은 `commentId` 지정.
5. **보고**: 이슈키 · 댓글 위치 한 줄.

---

## 거부 조건 (공통 + 모드별, 걸리면 중단·사유 보고)
- **[공통]** 결론(첫 줄) 없음 / 빈 내용 / 약어·코드 노출(→ 풀어쓰기·참고 격리) / Confluence를 평문 page ID로만 참조(→ 마크다운 링크).
- **[티켓]** 제목에 `[태그]` / 3시간 미만 잔작업을 독립 티켓으로 / `스토리`·`하위 작업` 생성.
- **[댓글]** 맥락 없는 "ok·완료" 한 단어 / 추적할 일을 댓글에만 두고 카드 안 만듦.

## Fallback (도구 미로드·연결 실패 시)
- ToolSearch/MCP(Atlassian Rovo) 로드·연결 실패로 발행 불가하면 → 카드/댓글 본문을 신 포맷 md로 작성해 **사용자에게 그대로 전달**하고, Jira 발행은 사람이 수동으로. (작성 포맷 정본은 이 스킬이므로 인계에 공백이 없다.)
