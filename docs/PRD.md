# UnitConverter_24 — PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| 버전 | 0.2.1 |
| 프로젝트 | UnitConverter_24 |
| 작성 일자 | 2026-06-05 |
| 문제 정의 | `report/01.UnitConvertor_ProblemDefinition_Report.md` |
| Mom Test 근거 | `prompting/01_UnitConvertor_MomTest_transcript.md` |

---

## 1. 제품 개요

### 1.1 한 줄 설명

CLI에서 `unit:value` 형식으로 길이를 입력하면, 지원 단위로 환산한 결과를 출력한다. 규칙·단위·계수는 **한곳(설정 파일·registry)** 에서 관리하고, **출력 포맷 선택·동적 단위 등록**을 지원하며, 실패 시 **원인별 메시지**와 **테스트**로 회귀를 막는다.

### 1.2 주제 (Mom Test, 솔루션 최소화)

입력 형식(`unit:value`)과 지원 단위 규칙이 한곳에서 드러나지 않아 실패·탐색·중단 비용이 큰 상황을, 실패 직후 원인·허용 형식이 분명해지고 단위 추가 시 수정 지점이 한곳으로 모이도록 줄인다.

### 1.3 대상 사용자

| 항목 | 내용 |
|------|------|
| **Role** | `src/cli.py` 및 `src/` 레이어를 실행·수정하는 학습자 |
| **Goal** | 지원 단위 변환 성공, 실패 시 이유 즉시 파악, 단위 추가 시 수정 위치 혼란 최소화 |

---

## 2. 문제 정의 (PRD 입력)

### 2.1 진짜 문제

입력 형식(`meter:2.5`)과 지원 단위가 코드 여러 곳에 묻혀 있어, 형식·단위 오류 시 동작 실패가 나고, 단위 추가 시 수정 위치 탐색에 시간이 많이 들며, 어려우면 작업을 중단한다.

### 2.2 표면 문제 (PRD 범위에서 제외하는 정의)

- 「길이 단위 변환 프로그램을 만든다」
- 「단위 추가 기능을 넣는다」

(기능 이름이 아니라 **분산 규칙 → 비용**을 줄이는 요구로 기술한다.)

### 2.3 Mom Test 증거

| # | 인용 | PRD 요구로의 연결 |
|---|------|-------------------|
| E1 | 다른 형식으로 넣어서 문제가 생겼어 | 입력 검증·형식 메시지 (FR-1) |
| E2 | 프로그램 미동작 / 미등록 단위 문제 | 단위 registry·unknown 처리 (FR-1, FR-2) |
| E3 | 그냥 멈췄어 / 수정할 곳 헷갈림 / 시간 오래 걸림 | 단일 수정 지점·TC (FR-2, FR-3, NFR-1) |

---

## 3. R-G-I-O

| 항목 | 스펙 |
|------|------|
| **Role** | 학습자 — CLI 실행 및 코드 수정 |
| **Goal** | 변환 성공, 실패 원인 명확화, 단위 추가 시 변경 지점 1곳 |
| **Input** | 한 줄 문자열 `unit:value` (예: `meter:2.5`) |
| **Output (성공)** | 지원 단위별 변환 결과 — 기본 **표 형태** 줄 (`{value} {unit} = {x} feet` 등), 선택 시 **JSON / CSV** (README 추가 요구사항) |
| **Output (실패)** | 형식 / 숫자 / unknown unit 구분 메시지 후 종료 |
| **Output (부가)** | 런타임 `1 cubit = 0.4572 meter` 등록 성공·실패 메시지 |

---

## 4. 범위

### 4.1 In Scope (PRD v0.2 · README 정합)

| ID | 내용 | README 근거 |
|----|------|-------------|
| IS-1 | `unit:value` 파싱 및 검증 (형식·숫자·단위) | 기본 요구사항 |
| IS-2 | meter, feet, yard 변환 및 CLI 출력 | 기본·비즈니스 로직 |
| IS-3 | 단위·계수 **단일 출처** (registry; 설정 파일과 동일 SSOT) | 품질·OCP |
| IS-4 | 변환·검증 **단위 테스트** (Test Loop) | 기본 요구사항 §4 |
| IS-5 | **Rule / Command / Test Loop** 문서화 및 구현 시 준수 | 8계층 |
| IS-6 | (선택) Cursor Skill 또는 `prompting/` 규칙 문서 | — |
| IS-7 | **출력 포맷 선택** — JSON / CSV / 표(기본) | 추가 요구사항 §출력 포맷 |
| IS-8 | **동적 단위 등록** — 예: `1 cubit = 0.4572 meter` 입력 후 변환에 사용 | 추가 요구사항 §동적 등록 |
| IS-9 | **설정 외부화** — 변환 비율·단위를 JSON/YAML에서 로드 | 추가 요구사항 §설정 외부화 |

> **구현 순서:** IS-1~IS-4·S1~S3(기본) → IS-9(설정 SSOT) → IS-8(동적 등록) → IS-7(출력 포맷). README Activities §4와 동일.

### 4.2 Out of Scope (본 PRD 제외)

| ID | 내용 | 비고 |
|----|------|------|
| OS-4 | GUI, 웹 API, 다국어 | — |
| OS-5 | Mom Test 미확인 지표 (멈춘 뒤 대안 도구 사용률, 정확한 분 단위 소요) | 후속 인터뷰 |
| OS-6 | 설정 **운영 배포**·핫리로드·원격 config 서버 | IS-9는 로컬 JSON/YAML 로드까지 |

---

## 5. 기능 요구사항 (Functional Requirements)

### FR-1 입력 검증 (S1)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-1.1 | `:` 없는 입력 거부 | `Invalid format`류 메시지 + `unit:value` 예시 |
| FR-1.2 | 비숫자 `value` 거부 | 숫자 오류 메시지에 잘못된 토큰 표시 |
| FR-1.3 | 미등록 `unit` 거부 | `Unknown unit` + **지원 단위 목록** 힌트 |
| FR-1.4 | (권장) 음수 값 정책 | README 품질 요구: 음수 검증 — 메시지 또는 거부 명시 |

### FR-2 변환 (S2)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-2.1 | meter 기준 환산 | `1 m = 3.28084 ft`, `1 m = 1.09361 yd` (README) |
| FR-2.2 | 입력 단위 → meter → 전 단위 출력 | `meter:2.5` 실행 시 meter/feet/yard 줄 출력 |
| FR-2.3 | 지원 단위 목록 단일 정의 | `main()`에 단위명·계수 하드코딩 **신규 추가 금지** (Rule R2) |

### FR-3 단위 확장 (S3)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-3.1 | 새 단위 1개 추가 시 변경 지점 1곳 | PRD·Command에 명시한 registry/설정만 diff |
| FR-3.2 | 기존 TC 회귀 없음 | 추가 전후 동일 TC green |
| FR-3.3 | OCP 방향 | 기존 변환·출력 코드 분기 확장 없이 registry 확장 |

### FR-4 출력 포맷 (IS-7 · README 추가)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-4.1 | 표 형태 기본 출력 | `meter:2.5` 시 README와 동일한 줄 단위 텍스트 |
| FR-4.2 | JSON 출력 선택 | 동일 변환 결과를 기계 판독 가능한 JSON으로 출력 |
| FR-4.3 | CSV 출력 선택 | 동일 변환 결과를 CSV(헤더·행)로 출력 |
| FR-4.4 | 포맷 선택 UX | CLI 인자·환경변수·실행 전 옵션 중 1가지 이상 — 문서화 |

### FR-5 동적 단위 등록 (IS-8 · README 추가)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-5.1 | 등록 입력 파싱 | `1 {unit} = {ratio} meter` 형태(README 예: `1 cubit = 0.4572 meter`) |
| FR-5.2 | 등록 후 변환 | 등록 직후(또는 동일 세션) `cubit:1` 등으로 변환·출력 가능 |
| FR-5.3 | SSOT 반영 | 등록 내용이 registry/설정 단일 출처에만 추가 (Rule R2·R3) |
| FR-5.4 | 등록 실패 처리 | 형식·숫자·중복 단위 등 구분 메시지 (S1 정합) |

### FR-6 설정 외부화 (IS-9 · README 추가)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| FR-6.1 | JSON 또는 YAML 로드 | meter/feet/yard(및 등록 단위) 비율을 파일에서 읽음 |
| FR-6.2 | 기본값 폴백 | 설정 파일 없거나 손상 시 README 비율로 동작 또는 명확한 오류 |
| FR-6.3 | 코드 내 리터럴 금지 | FR-2.3·Rule R2 — 계수는 파일·registry만 |
| FR-6.4 | TC | 로드 성공·unknown unit·동적 등록과 회귀 TC |

---

## 6. 비기능 요구사항 (Non-Functional)

| ID | 요구 | 수용 기준 |
|----|------|-----------|
| NFR-1 | Test Loop | 최소 4 TC: 형식 오류, unknown unit, 숫자 오류, 정상 변환 |
| NFR-2 | SRP | parse / convert / print 책임 분리 |
| NFR-3 | Discoverability | 지원 단위·입력 형식을 README + 실패 메시지 + (가능 시) `--help`에서 동일하게 안내 |
| NFR-4 | 변경 최소화 | README: 새 단위 추가 시 기존 코드 변경 최소화 |
| NFR-5 | 포맷 일관성 | 표/JSON/CSV가 **동일 변환 결과**를 표현 (값만 직렬화 차이) |
| NFR-6 | 설정·코드 단일 진실 | 동적 등록·파일 로드가 서로 다른 계수 사본을 만들지 않음 |

---

## 7. Rule · Command · Test Loop (8계층 — 이번 세션)

구현·리뷰 시 **필수 준수**. 상세는 `report/01.UnitConvertor_ProblemDefinition_Report.md` §7.

### 7.1 Rule (요약)

- R1: `unit:value` 계약, 오류 유형별 메시지 분리
- R2: 단위·계수 단일 출처, `main()` 분기 추가 금지
- R3: 단위 추가는 명시된 파일/블록만
- R4: 표면 문제 정의 시 진짜 문제 문장으로 복귀
- R5: README 비율 준수

### 7.2 Command (요약)

C1 분산 지점 목록 → C2 단일 출처 → C3 `main()` 슬림화 → C4 TC 선작성 → C5 green + 1파일 diff 검증 → **C6** README 추가(FR-4~6) TC 선행·구현 (M4)

### 7.3 Test Loop (요약)

Red (4 TC 기본) → Green (registry·설정 SSOT) → Refactor (단위 1개 mock TC) → Exit (S1~S3) → **Red/Green (FR-4~6 TC)** → Exit (S4)

### 7.4 Skill (선택)

트리거: UnitConverter, Mom Test, 단위 추가. 본 PRD의 §2·§8·§7을 스킬 본문에 포함.

---

## 8. 성공 기준 (수용 테스트)

| ID | 기준 | Mom Test |
|----|------|----------|
| **S1** | 형식·숫자·unknown 구분 메시지 + 힌트 | E1, E2 |
| **S2** | meter/feet/yard 변환 TC green, 회귀 시 실패 | E2 |
| **S3** | 단위 추가 diff 1파일(또는 1 registry), 문서화된 수정 경로 | E3 |
| **S4** | README 추가 요구 3종(FR-4~6) TC green, 포맷·등록·설정 로드 검증 | README Activities §4 |

### 8.1 Test Loop 최소 TC 매트릭스 (기본 · S1~S2)

| 입력 | 기대 |
|------|------|
| `meter:2.5` | 3단위 변환 출력 또는 구조화된 결과; 수치 TC로 검증 |
| `meter` (콜론 없음) | 형식 오류, exit |
| `inch:1` | unknown unit, 지원 목록 힌트 |
| `meter:abc` | 숫자 오류 |

### 8.2 Test Loop TC 매트릭스 (추가 · S4 · FR-4~6)

| 영역 | 입력/조건 | 기대 |
|------|-----------|------|
| FR-6 | `units.json`(또는 `.yaml`)에 README 비율 | meter/feet/yard 변환 TC green |
| FR-5 | `1 cubit = 0.4572 meter` 등록 후 `cubit:1` | cubit 포함 전 단위 출력 |
| FR-4 | 동일 입력, `--format json` (또는 문서화된 옵션) | JSON에 3단위 이상 결과 |
| FR-4 | `--format csv` | CSV 헤더·데이터 행 |
| FR-4 | 기본(표) | §8.1 `meter:2.5` 줄 출력 유지 |

---

## 9. 사용자 시나리오

### 9.1 Happy path

1. 사용자가 `python src/cli.py` 실행
2. `meter:2.5` 입력
3. meter·feet·yard 변환 줄 출력

### 9.2 형식 오류 (E1)

1. `2.5 meter` 등 잘못된 형식 입력
2. 형식 오류 메시지와 `unit:value` 예시 확인
3. (학습 목표) 재시도 가능 — 메시지만으로 규칙 파악

### 9.3 미등록 단위 (E2)

1. `inch:12` 입력
2. unknown unit + 지원 단위 목록
3. TC로 동일 동작 고정

### 9.4 단위 추가 (E3)

1. registry(또는 설정)에 단위 1줄 추가
2. TC 1건 추가 또는 기대값 확장
3. 기존 TC green, diff 1파일 원칙 확인

### 9.5 설정 파일 로드 (IS-9)

1. `units.json`(또는 YAML)에 meter/feet/yard 비율 정의
2. 앱 시작 시 로드 후 `meter:2.5` 변환
3. TC로 파일 로드·README 비율 일치 검증

### 9.6 동적 단위 등록 (IS-8)

1. `1 cubit = 0.4572 meter` 입력(또는 전용 CLI 모드)
2. `cubit:2` 변환 시 cubit·meter·feet·yard 등 출력
3. registry에만 반영, `main()` 분기 추가 없음 (S3)

### 9.7 출력 포맷 선택 (IS-7)

1. `meter:2.5` 기본 실행 → 표 형태 줄 출력
2. JSON·CSV 옵션 실행 → 동일 수치, 형식만 변경
3. TC로 3포맷 결과 동등성 검증 (NFR-5)

---

## 10. 의존성 및 참조

### 10.1 프로젝트 구조 (레이어)

```text
config/units.json
src/cli.py              # CLI 진입 (I/O·옵션)
src/domain/             # 파싱·검증·변환·registry
src/infrastructure/     # 설정 로드 → domain
src/application/        # use_cases (시나리오)
tests/domain|application|infrastructure/
```

의존: `cli` → `application` → `domain` · `infrastructure` → `domain`.

### 10.2 참조 문서

| 자료 | 용도 |
|------|------|
| `README.md` | 기본·품질·추가 요구사항, 비율, 실행 방법 |
| `src/cli.py` | CLI 진입점 (구 `UnitConverter.py` 대체) |
| `config/units.json` | 단위·비율 SSOT (FR-6) |
| `report/01_UnitConvertor_MomTest_report.md` | Pain 분석 |
| `report/01.UnitConvertor_ProblemDefinition_Report.md` | 문제·8계층 정의 |

---

## 11. 마일스톤 (제안)

| 단계 | 산출 | 완료 조건 |
|------|------|-----------|
| M0 | PRD + 문제 정의 보고서 | 본 문서·report 승인 |
| M1 | Test Loop Red | 4 TC 작성, 일부 실패 허용 |
| M2 | FR-1, FR-2, NFR-1,2 | TC green, S1·S2 |
| M3 | FR-3 | 단위 1개 추가 드라이런, S3 |
| M4 | FR-6, FR-5, FR-4 (권장 순) | 설정 로드 → 동적 등록 → 출력 포맷; S4·README §4 Activities |
| M5 | (선택) Skill·Hook | Rule 자동 검사 |

---

## 12. 리스크 및 가정

| 리스크 | 완화 |
|--------|------|
| 에러 메시지만 개선하고 구조는 그대로 | S3·FR-3·Rule R2로 registry 필수 |
| 기본·추가 요구를 한꺼번에 구현해 TC 붕괴 | M2(S1~S3) 완료 후 M4; §4.1 구현 순서 |
| 포맷·설정·동적 등록이 서로 다른 계수 사본 유지 | NFR-6·FR-6.3·단일 registry |
| 학습자가 여전히 코드 전체 탐색 | Command C2 단일 출처 + 문서에 경로 고정 |

**가정:** 학습자는 Python CLI 실행 가능; pytest(또는 unittest) 사용 가능.

---

## 13. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-06-05 | Mom Test 기반 초안 — 문제 정의, R-G-I-O, S1~S3, Rule/Command/Test Loop, 범위 |
| 0.2 | 2026-06-05 | README 추가 요구 3종 In Scope(IS-7~9): OS-1~3 제거, FR-4~6·S4·§8.2·§9.5~9.7·M4 반영 |
| 0.2.1 | 2026-06-05 | 레이어 구조: `src/{cli,domain,infrastructure,application}`, `config/units.json`, tests 하위 분리 |
