# UnitConverter_24 — Harness·Rules·구조 세션 Export Transcript

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-05 |
| 세션 | pytest Harness · `.cursorrules` · PRD v0.2/v0.2.1 · 레이어 스캐폴드 · PR |
| 선행 Transcript | `prompting/02_UnitConvertor_ProblemDefinition_transcript.md` |
| 참조 PRD | `docs/PRD.md` v0.2.1 (§10.1 구조, IS-7~9 In Scope) |
| PR | [spec → main #1](https://github.com/hyundang/UnitConverter_24/pull/1) |
| Agent 세션 ID | `2a8d745d-aeb6-40ad-a2ca-7f64d19805ff` (초기 Harness) |

---

## 세션 범위 (누적)

| 단계 | In | Out |
|------|----|-----|
| Turn 1~2 | Harness 골격, `.cursorrules` | 구현·assert, commit |
| Turn 4~5 | PRD OS-1~3 → In Scope | 코드 구현 |
| Turn 6~7 | 커밋 제목 제안, GitHub PR | — |
| Turn 8~12 | 레이어 구조 설계(Ask) | — |
| Turn 13 | `src/` 레이어 스캐폴드 | domain 로직·RED TC |

---

## 대화 본문

### Turn 1 — 최소 Harness 요청

**사용자:** 최소 Harness를 만들어줘. 코드·테스트 본문은 아직 작성하지 마. Harness 골격만.

**에이전트:** `docs/PRD.md` §8.1·`prompting/02` Test Loop Red 제안 확인 후 pytest Harness 추가.

**산출:**

| 파일 | 역할 |
|------|------|
| `pytest.ini` | `testpaths=tests`, markers `prd_s1`~`prd_s3` |
| `requirements-dev.txt` | `pytest>=8.0` |
| `tests/inputs.py` | PRD §8.1 입력 상수 4개 |
| `tests/conftest.py` | `prd_inputs`, `supported_units` fixture |
| `tests/test_validation.py` | S1 슬롯 3 (skip) |
| `tests/test_conversion.py` | S2 슬롯 1 (skip) |

**결과:** 4 collected, 4 skipped (`Harness skeleton — Test Loop Red`).

---

### Turn 2 — `.cursorrules` 초안

**사용자:** 루트 `.cursorrules` 40~80줄 — 도메인 CLI, TDD RED→GREEN→REFACTOR, skip/xfail 금지, SSOT, 한국어·Phase/Layer/Track, git은 요청 시만. 다른 파일 금지.

**에이전트:** `.cursorrules` **45줄** 생성 (도메인·설계·MagicConstant·TDD·AI 행동·금지).

---

### Turn 3 — transcript export (초안)

**사용자:** prompting 폴더에 지금까지 대화 저장.

**에이전트:** 본 문서 초안 저장.

---

### Turn 4 — PRD v0.2 범위 확장

**사용자:** PRD §4.2 OS-1~OS-3(README 추가 요구)을 이번 PRD In Scope에 포함. 연관 문서 일괄 수정.

**에이전트:**

| 변경 | 내용 |
|------|------|
| **In Scope** | IS-7 출력 포맷, IS-8 동적 등록, IS-9 설정 JSON/YAML |
| **Out of Scope** | OS-4 GUI/웹, OS-5 Mom Test 미확인, OS-6 운영 배포 |
| **추가** | FR-4~6, S4, §8.2 TC, §9.5~9.7, M4, NFR-5~6 |
| **연동 수정** | `report/01.UnitConvertor_ProblemDefinition_Report.md`, `.cursorrules`, `prompting/02` v0.2 정정 각주 |

**구현 순서:** M2(S1~S3) → M4(IS-9 → IS-8 → IS-7).

---

### Turn 5 — 커밋 제목 (Ask)

**사용자:** 현재 브랜치 변경에 맞는 영어 커밋 제목.

**에이전트 (권장):**

```text
feat: Add pytest harness skeleton, Cursor rules, and PRD v0.2 scope
```

대안: docs 중심 / test 중심 / 2-commit 분리 제안.

---

### Turn 6 — GitHub PR (spec → main)

**사용자:** GitHub MCP로 spec → main PR 생성.

**에이전트:** PR 생성 완료.

- **URL:** https://github.com/hyundang/UnitConverter_24/pull/1  
- **제목:** `feat: Add pytest harness skeleton, Cursor rules, and PRD v0.2 scope`  
- **커밋:** `0e0a4e9` (origin/spec, main 대비 +1)  
- **변경:** 13 files, +1046 (Harness, PRD, report, prompting, `.cursorrules`; `UnitConverter.py` 구현 변경 없음)

---

### Turn 7~12 — 프로젝트 구조 논의 (Ask)

**사용자 의도 (확정):**

| 항목 | 결정 |
|------|------|
| 레이어 | `domain` · `infrastructure` · `application` |
| `unit_converter/` 중간 패키지 | **없음** |
| CLI | **`src/cli.py`** (루트 `cli.py`·`UnitConverter.py` 아님) |
| `app` 폴더명 | **`application`** |
| `cli/` 폴더 | **없음** — `src/cli.py` 단일 파일 |

**의존 방향:**

```text
src/cli.py  →  application
application  →  domain, infrastructure
infrastructure  →  domain
domain  →  (상위 import 없음)
```

**실행:** `python src/cli.py` · `pytest.ini` → `pythonpath = . src`

**에이전트 권장 (요약):**

- domain: 파싱·검증·변환·registry  
- infrastructure: `config/units.json` 로드  
- application: `use_cases.py`  
- formatting: 이후 `application/formatting/` 또는 동등 위치  

---

### Turn 13 — 레이어 스캐폴드 (구현 없음)

**사용자:** 위 구조로 변경. 코드 작성 없이 폴더·골격만. 관련 파일 수정.

**에이전트 산출:**

```text
config/units.json              # {}
src/cli.py                     # docstring only
src/domain/__init__.py
src/infrastructure/__init__.py
src/application/use_cases.py   # docstring only
tests/test_cli.py
tests/domain/test_validation.py   # Harness (tests/에서 이동)
tests/domain/test_conversion.py
tests/application/__init__.py
tests/infrastructure/__init__.py
```

**문서·설정 수정:**

| 파일 | 변경 |
|------|------|
| `pytest.ini` | `pythonpath = . src` |
| `README.md` | 구조 트리, `python src/cli.py` |
| `docs/PRD.md` | v0.2.1, §10.1 구조, Role·§9.1·참조 |
| `.cursorrules` | `src/cli.py`, 레이어 Layer 선언 |
| `report/01.UnitConvertor_ProblemDefinition_Report.md` | Role, C1~C3, 레거시→목표 구조 |

**검증:** `pytest --collect-only` → 4 tests (`tests/domain/`).

**미구현:** domain/infrastructure/application 본문, `cli.py` `main()`, RED assert, `units.json` 비율 데이터.

---

### Turn 14 — transcript 갱신 (본 요청)

**사용자:** `prompting/03_UnitConvertor_HarnessAndRules_transcript.md` 대화 내용 업데이트.

**에이전트:** Turn 4~14 및 최종 구조·체크리스트 반영 (본 문서).

---

## 최종 프로젝트 구조

```text
UnitConverter_24/
├── config/units.json
├── src/
│   ├── cli.py
│   ├── domain/
│   ├── infrastructure/
│   └── application/
│       └── use_cases.py
├── tests/
│   ├── conftest.py, inputs.py
│   ├── test_cli.py
│   ├── domain/          # §8.1 Harness (4 skip)
│   ├── application/
│   └── infrastructure/
├── docs/PRD.md          # v0.2.1
├── .cursorrules
├── pytest.ini
└── README.md
```

---

## 정합·미결 (후속)

| 항목 | 상태 | 조치 |
|------|------|------|
| Harness 4 TC skip | 임시 | RED 시 skip 제거 (`.cursorrules` 금지) |
| `UnitConverter.py` | 레거시/빈 파일 가능 | 삭제 또는 README에서 완전 제거 확인 |
| PR #1 | spec → main | 머지 후 구조 커밋은 별도 PR/브랜치 |
| registry SSOT | `config/units.json` 빈 객체 | FR-6·M4에서 README 비율 반영 |
| RED TC | 미작성 | `tests/domain/` assert + `src/domain` 구현 |

---

## 체크리스트 (누적)

| 항목 | 완료 |
|------|------|
| pytest Harness + 4 TC 슬롯 | ✅ |
| `.cursorrules` | ✅ |
| PRD v0.2 (IS-7~9, FR-4~6, S4) | ✅ |
| PRD v0.2.1 (§10.1 구조) | ✅ |
| report / README / pytest 경로 | ✅ |
| GitHub PR #1 (spec→main) | ✅ |
| `src/` 레이어 스캐폴드 | ✅ |
| tests → `tests/domain/` | ✅ |
| TC assert · domain 구현 | ❌ |
| Harness skip 제거 | ❌ |

---

## 문서 맵

```text
prompting/01_UnitConvertor_MomTest_transcript.md
prompting/02_UnitConvertor_ProblemDefinition_transcript.md  (+ PRD v0.2 정정 각주)
prompting/03_UnitConvertor_HarnessAndRules_transcript.md     ← 본 Export (갱신)
report/01.UnitConvertor_ProblemDefinition_Report.md
docs/PRD.md                                                  # v0.2.1
.cursorrules
config/units.json
src/{cli,domain,infrastructure,application}
tests/
```

---

## 다음 세션 제안

1. **RED** `Track: S1-validation` — `tests/domain/test_validation.py` skip 제거, `src/domain` 검증  
2. **RED** `Track: S2-conversion` — 변환 assert, `src/domain/conversion.py`  
3. **GREEN** `Track: S3-registry` — `config/units.json` + `infrastructure` 로더, `application` 연동  
4. **M4** FR-4~6 (설정 → 동적 등록 → 포맷), S4 TC  
5. PR #1 머지 후 구조 스캐폴드 커밋을 `main` 또는 `red` 브랜치에 반영
