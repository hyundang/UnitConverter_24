# UnitConverter_24 — 문제 정의·PRD 세션 Export Transcript

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-05 |
| 세션 | Mom Test 결과 → 문제 정의·8계층·문서화 |
| 선행 Transcript | `prompting/01_UnitConvertor_MomTest_transcript.md` |
| 산출 보고서 | `report/01.UnitConvertor_ProblemDefinition_Report.md` |
| 산출 PRD | `docs/PRD.md` |
| 규칙 | 솔루션 이름 최소화, Mom Test 증거와 성공 기준 연결 |

---

## 세션 입력 (사용자 제공 초안)

### 표면 문제 (잘못된 정의)

「길이 단위 변환 프로그램을 만든다」「단위 추가 기능을 넣는다」처럼, 제품·기능 이름으로 문제를 정의하는 것.

### 진짜 문제 (한 문장)

입력 형식(`meter:2.5`)과 지원 단위가 코드 여러 곳에 묻혀 있어, 형식을 틀리거나 미등록 단위를 쓰면 동작 실패가 나고, 단위를 추가할 때 어디를 고쳐야 하는지 찾는 데 시간이 많이 들며, 어려우면 작업을 그만둔다.

### Mom Test 증거 3줄

1. 「다른 형식으로 넣어서 문제가 생겼어」
2. 「프로그램이 제대로 동작하지 않았어」 / 「등록하지 않은 단위로 변환하려고 했더니 역시 문제가 발생했어」
3. 「그냥 멈췄어」 / 「변환 단위가 추가될 때마다 기존 코드를 수정할 곳이 많아서 헷갈렸어」 / 「끝냈지만 시간이 오래걸렸어」

### 요청 산출물 (4블록 + 8계층)

1. 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2. R-G-I-O (Role / Goal / Input / Output)
3. 성공 기준 3개 (Mom Test 증거와 연결)
4. 표면 문제 — 이번 프로젝트에서 하지 않을 것
5. 8계층 중 이번 세션: **Rule, Command, (Skill), Test Loop** 만

---

## 대화 본문

### Turn 1 — 문제 정의 초안 요청

**사용자:** 위 Mom Test 초안을 바탕으로 (1)~(4)와 8계층(Rule/Command/Skill/Test Loop)을 정리해 달라.

**에이전트:** 코드·`01` Transcript·Mom Test 보고서를 확인한 뒤 아래 초안을 제시했다.

---

### Turn 1 — 에이전트 응답 요약

#### 1) 주제 한 문장

입력 형식(`unit:value`)과 지원 단위 규칙이 한곳에서 드러나지 않아 실패·탐색·중단 비용이 큰 상황을, 실패 직후 원인·허용 형식이 분명해지고 단위 추가 시 수정 지점이 한곳으로 모이도록 줄인다.

#### 2) R-G-I-O

| 항목 | 내용 |
|------|------|
| **Role** | `UnitConverter.py`를 실행·수정하는 학습자 |
| **Goal** | 지원 단위면 변환 성공; 실패 시 이유 즉시 파악; 단위 추가 시 수정 위치 혼란 최소화 |
| **Input** | CLI `unit:value` (예: `meter:2.5`); 지원: meter, feet, yard |
| **Output** | 성공: 3단위 변환 줄 / 실패: 형식·숫자·unknown 구분 메시지 |

#### 3) 성공 기준 3개

| # | 기준 | Mom Test 연결 |
|---|------|---------------|
| **S1** | 형식·숫자·unknown 메시지 구분 + 허용 형식·지원 단위 힌트 | E1, E2 |
| **S2** | 3단위 변환 TC green, 회귀 즉시 감지 | E2 |
| **S3** | 단위 추가 시 변경 지점 1곳 문서화; `if/elif` 다중 복붙 금지 | E3 |

#### 4) 하지 않을 것

- 「변환 프로그램/단위 추가 기능」만으로 문제 정의
- README 추가 요구사항(JSON/CSV, cubit 동적 등록 등) 이번 세션 일괄 구현
- OCP/SRP 용어만으로 완료 선언
- 에러 메시지 1줄만으로 해결 주장
- Mom Test 미확인 항목을 필수 성공 기준에 포함

#### 5) 8계층 (이번 세션만)

**Rule:** R1 `unit:value` 계약·오류 유형별 메시지 / R2 단위·계수 단일 출처 / R3 수정 허용 경로만 / R4 표면 문제 시 진짜 문제로 복귀 / R5 README 비율

**Command:** C1 분산 지점 목록 → C2 단일 출처 → C3 `main()` 슬림화 → C4 TC 선작성 → C5 green + 1파일 diff

**Skill (선택):** 트리거·진짜 문제·S1~S3·Test Loop — `.cursor/rules` 또는 `prompting/` 대안 가능

**Test Loop:** Red(4 TC) → Green(registry) → Refactor(단위 1개 mock) → Exit(S1~S3)

---

### Turn 2 — 문서 생성 요청

**사용자:** `report/01.UnitConvertor_ProblemDefinition_Report.md`와 `docs/PRD.md`를 위 초안으로 생성해 달라.

**에이전트:** 두 파일 생성 완료.

| 파일 | 역할 |
|------|------|
| `report/01.UnitConvertor_ProblemDefinition_Report.md` | 문제 정의·R-G-I-O·S1~S3·8계층·코드 연결·다이어그램 |
| `docs/PRD.md` | FR/NFR·범위 In/Out·시나리오·TC 매트릭스·마일스톤 |

---

### Turn 3 — Export Transcript 저장 (본 문서)

**사용자:** `prompting/` 아래 `02_UnitConvertor_[적절한단어]` 형식으로 export transcript 저장.

**에이전트:** 본 파일 `02_UnitConvertor_ProblemDefinition_transcript.md` 생성.

---

## 세션 종료 요약 (Export)

### 1. 주제 한 문장

입력 형식(`unit:value`)과 지원 단위 규칙이 한곳에서 드러나지 않아 실패·탐색·중단 비용이 큰 상황을, 실패 직후 원인·허용 형식이 분명해지고 단위 추가 시 수정 지점이 한곳으로 모이도록 줄인다.

### 2. R-G-I-O

- **Role:** 학습자 (`UnitConverter.py` 실행·수정)
- **Goal:** 변환 성공, 실패 원인 명확, 단위 추가 위치 단일화
- **Input:** `unit:value`
- **Output:** 변환 줄 또는 구분된 오류 메시지

### 3. 성공 기준

- **S1** — 검증 메시지·힌트 (E1, E2)
- **S2** — 변환 TC (E2)
- **S3** — 단일 수정 지점 (E3)

### 4. 표면 문제 (하지 않을 것)

기능 이름 중심 정의; README 추가기능 일괄; 용어만 회고; 메시지만 패치

### 5. 8계층 산출

Rule · Command · (Skill) · Test Loop — 구현은 M1~M3, 문서는 report·PRD

### 6. 문서 맵

```text
prompting/01_UnitConvertor_MomTest_transcript.md     ← 인터뷰 원본
prompting/02_UnitConvertor_ProblemDefinition_transcript.md  ← 본 Export
report/01_UnitConvertor_MomTest_report.md            ← Mom Test 분석
report/01.UnitConvertor_ProblemDefinition_Report.md  ← 문제·8계층
docs/PRD.md                                          ← 요구사항
```

---

## 체크리스트

| 항목 | 완료 |
|------|------|
| Mom Test 증거 → S1~S3 매핑 | ✅ |
| 솔루션 최소화 주제 1문장 | ✅ |
| R-G-I-O | ✅ |
| 표면 문제 / Out of Scope | ✅ |
| Rule · Command · Skill · Test Loop | ✅ |
| Problem Definition Report | ✅ |
| PRD v0.1 → v0.2 (IS-7~9 In Scope) | ✅ / 정정 §하단 |
| Export Transcript (본 문서) | ✅ |

---

## 다음 세션 제안 (참고)

- Test Loop **Red**: `tests/`에 4 TC 추가
- Command **C2~C5**: registry 리팩터 + TC green
- Skill: `.cursor/rules` 또는 전용 skill 파일 (선택)

---

## PRD v0.2 정정 (2026-06-05)

본 Export 당시 Turn 1의 「README 추가 요구 일괄 구현 금지」는 **`docs/PRD.md` v0.2**에서 변경됨.

- **In Scope:** IS-7(출력 포맷), IS-8(동적 등록), IS-9(설정 JSON/YAML) — 구 README OS-1~3
- **성공 기준:** S4, FR-4~6, M4
- **여전히 Out of Scope:** OS-4(GUI·웹), OS-5(Mom Test 미확인 지표), OS-6(운영 배포)
