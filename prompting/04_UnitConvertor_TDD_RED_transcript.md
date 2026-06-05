# UnitConverter_24 — Dual-Track TDD RED 세션 Export Transcript

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-05 |
| 세션 | Dual-Track TDD **RED 전체** — Logic(D-01~D-10) · UI(D-07~09, U-01~04) |
| 선행 Transcript | `prompting/03_UnitConvertor_HarnessAndRules_transcript.md` |
| 참조 PRD | `docs/PRD.md` v0.2.2 (§5.0 application 파싱, §8.1~8.2, §9.1~9.7) |
| 참조 Skill | `.cursor/skills/unit-converter-tdd/SKILL.md`, `reference.md` |
| Agent 세션 | Cursor TDD RED 커맨드 (`/tdd-red`) 반복 실행 |

---

## 세션 범위

| 단계 | In | Out |
|------|----|-----|
| RED 설계표 | C2C·Track B·테스트 플랜·ECB (파일 미생성) | `src/` 구현 |
| RED 구현 | `tests/` assert·fixture·pytest FAIL/ERROR 확인 | GREEN·REFACTOR |
| Harness 수정 | `tests/cli` 수집 문제 해결 | — |
| 문서화 | 본 transcript · RED 보고서 | commit/push (미요청) |

**Phase 선언 규칙:** `Phase: red | Layer: <…> | Track: <Logic|UI> | ID: <D-*/U-*>`

---

## 대화 본문

### Turn 1 — D-01 RED 설계 (표만)

**사용자:** `/tdd-red` — Phase: red, Track: Logic, Layer: domain, D-01. C2C·Track B·테스트 플랜·ECB 표 작성. `tests/`·`src/` 만들지 마.

**에이전트:** PRD S2·§8.1, FR-2, Rule R1~R3 기준 설계표 작성.

**핵심 결정:**
- Arrange SSOT = `conftest` `default_registry` (README 3단위 in-memory)
- `config/units.json` 로드는 D-05(infrastructure)로 미룸
- 대상 API: `domain.conversion.convert_all`, `domain.registry.UnitRegistry`
- 파일: `tests/domain/test_d_01.py`

---

### Turn 2 — D-01 RED 구현

**사용자:** RED 단계만 진행해줘.

**에이전트:** RED Harness 구현.

| 파일 | 내용 |
|------|------|
| `tests/inputs.py` | README 비율·PRD §8.1 입력 SSOT |
| `tests/conftest.py` | `default_registry`, `supported_units`, `prd_s2_input` |
| `tests/domain/test_d_01.py` | `test_meter_2_5_converts_to_all_supported_units` |

**pytest:** `ModuleNotFoundError: No module named 'domain.conversion'` → RED 완료.

---

### Turn 3 — D-02~D-04 RED 설계 (표만)

**사용자:** `/tdd-red` — application+domain, D-02~D-04. 표만.

**에이전트:** PRD §5.0 반영 — 파싱=application, 검증=domain.

| ID | Layer | API |
|----|-------|-----|
| D-02 | application | `parse_unit_value` → `FormatError` |
| D-03 | domain | `validate_unit` → `UnknownUnitError` |
| D-04 | application | `parse_unit_value` → `NumberError` |

---

### Turn 4 — D-02~D-04 RED 구현

**사용자:** RED 단계 진행해줘.

**에이전트:**

| 파일 | 테스트 |
|------|--------|
| `tests/application/test_d_02.py` | `test_rejects_missing_colon_format` |
| `tests/domain/test_d_03.py` | `test_rejects_unknown_unit_with_supported_units_hint` |
| `tests/application/test_d_04.py` | `test_rejects_non_numeric_value_token` |

**pytest:** 3 error (application.parsing / domain.validation 미구현).

---

### Turn 5 — D-07~D-09 RED 설계 (표만)

**사용자:** `/tdd-red` — UI/cli, D-07~09. 표만. (요청 경로 `tests/cli/`)

**에이전트:** FR-4·§8.2·NFR-5 기준 subprocess CLI 설계. `tests/cli/test_d_07~09.py` 계획.

---

### Turn 6 — D-07~D-09 RED 구현

**사용자:** RED 단계 진행해줘.

**에이전트:**

| 파일 | 테스트 |
|------|--------|
| `tests/cli/test_d_07.py` | JSON `--format json` |
| `tests/cli/test_d_08.py` | CSV `--format csv` |
| `tests/cli/test_d_09.py` | 기본 표 출력 |
| `pytest.ini` | `prd_s4` 마커 추가 |

**pytest:** 3 failed (cli 미구현, stdout 빈 문자열).

---

### Turn 7 — pytest `tests/cli` 미실행 문제 (Ask → Agent)

**사용자:** `python -m pytest` 시 `tests/cli` 테스트가 안 돼.

**에이전트 분석:**
1. Logic TC 수집 ERROR(미구현 import)가 **전체 세션 중단** (기본 pytest 동작)
2. `tests/cli/` vs `src/cli.py` 이름 충돌 잠재 위험

**해결 (Turn 8):**
- `pytest.ini` → `addopts = -ra --continue-on-collection-errors`
- `tests/cli/` → **`tests/test_cli/`** 이동 (reference.md UI Track 정렬)
- `tests/__init__.py` 추가

---

### Turn 8 — D-05 RED 설계 (표만)

**사용자:** `/tdd-red` — infrastructure, D-05. 표만.

**에이전트:** FR-6·§8.2. `load_registry` + `convert_all` 통합. Arrange = `tmp_path` JSON fixture.

---

### Turn 9 — D-05 RED 구현

**에이전트:** `tests/infrastructure/test_d_05.py`, conftest `readme_units_json`.

**pytest:** `ModuleNotFoundError: No module named 'infrastructure.config_loader'`.

---

### Turn 10 — D-06 RED 구현

**사용자:** RED 단계 진행해줘. (M4 순서 다음 항목)

**에이전트:** `tests/application/test_d_06.py` — `register_unit_from_string` + `convert_all(cubit:1)`.

**pytest:** `ImportError: cannot import name 'register_unit_from_string'`.

---

### Turn 11 — D-10 RED 설계 (표만)

**사용자:** `/tdd-red` — domain, D-10. 표만. (요청에 FR-6 오기 → FR-3·S3로 정정)

**에이전트:** S3 mock 단위 `fathom`, registry 확장 OCP, D-01 회귀 assert 포함.

---

### Turn 12 — D-10 RED 구현

**에이전트:** `tests/domain/test_d_10.py`, `registry_with_fathom` fixture.

**pytest:** `ModuleNotFoundError: No module named 'domain.conversion'`.

---

### Turn 13 — U-01~U-04 RED 설계 (표만)

**사용자:** `/tdd-red` — UI/cli, U-01~04. 표만.

**에이전트:** §9.1~9.7 사용자 시나리오 E2E. 경로 `tests/test_cli/test_u_*.py`.

---

### Turn 14 — U-01~U-04 RED 구현

**에이전트:**

| ID | 파일 | 시나리오 |
|----|------|----------|
| U-01 | `test_u_01.py` | §9.1 Happy path |
| U-02 | `test_u_02.py` | §9.2 형식 오류 |
| U-03 | `test_u_03.py` | §9.6 동적 등록 multiline |
| U-04 | `test_u_04.py` | §9.7 3포맷 NFR-5 |

**pytest:** 4 failed (cli 미구현).

---

### Turn 15 — transcript·보고서 저장 (본 요청)

**사용자:** 현재까지 대화내용을 prompting 폴더 아래 저장하고, 보고서로 만들어서 report 폴더 아래 저장해줘.

**에이전트:** `prompting/04_*.md`, `report/02_*.md` 작성.

---

## 최종 Harness 구조 (RED 완료 시점)

```text
tests/
  __init__.py
  inputs.py                    # PRD·README·FR-5·S3·U-* SSOT
  conftest.py                  # registry·cli·json·cubit·fathom fixtures
  domain/
    test_d_01.py               # S2 변환
    test_d_03.py               # S1 unknown
    test_d_10.py               # S3 registry 확장
  application/
    test_d_02.py               # S1 형식
    test_d_04.py               # S1 숫자
    test_d_06.py               # FR-5 등록
  infrastructure/
    test_d_05.py               # FR-6 config 로드
  test_cli/
    test_d_07.py ~ test_d_09.py  # FR-4 포맷
    test_u_01.py ~ test_u_04.py  # §9 사용자 시나리오
```

---

## pytest RED 최종 상태 (2026-06-05)

| 구분 | 수집 | 실행 결과 | 비고 |
|------|------|-----------|------|
| Logic (D-01~06, D-10) | 7 TC | **7 error** (import 미구현) | `--continue-on-collection-errors` |
| Infrastructure (D-05) | 1 TC | **1 error** | |
| UI D-07~09 | 3 TC | **3 failed** | |
| UI U-01~04 | 4 TC | **4 failed** | |
| **합계** | **15 TC** | error 8 + failed 7 | skip 0 |

**일괄 실행:**

```bash
python -m pytest -v
```

---

## RED ID 매핑 완료 체크리스트

| ID | RED | 테스트 파일 |
|----|-----|-------------|
| D-01 | ✅ | `tests/domain/test_d_01.py` |
| D-02 | ✅ | `tests/application/test_d_02.py` |
| D-03 | ✅ | `tests/domain/test_d_03.py` |
| D-04 | ✅ | `tests/application/test_d_04.py` |
| D-05 | ✅ | `tests/infrastructure/test_d_05.py` |
| D-06 | ✅ | `tests/application/test_d_06.py` |
| D-07 | ✅ | `tests/test_cli/test_d_07.py` |
| D-08 | ✅ | `tests/test_cli/test_d_08.py` |
| D-09 | ✅ | `tests/test_cli/test_d_09.py` |
| D-10 | ✅ | `tests/domain/test_d_10.py` |
| U-01 | ✅ | `tests/test_cli/test_u_01.py` |
| U-02 | ✅ | `tests/test_cli/test_u_02.py` |
| U-03 | ✅ | `tests/test_cli/test_u_03.py` |
| U-04 | ✅ | `tests/test_cli/test_u_04.py` |

---

## 미완 · 다음 단계

| 항목 | 상태 |
|------|------|
| GREEN (`src/domain`, `application`, `infrastructure`, `cli`) | **미착수** |
| REFACTOR (S3 diff 1파일 체크리스트) | GREEN 후 |
| `config/units.json` README 비율 | `{}` (GREEN 시 반영) |
| git commit / push | 사용자 요청 시만 |

---

## 부록: 문서 관계

| 문서 | 역할 |
|------|------|
| `prompting/04_UnitConvertor_TDD_RED_transcript.md` | 본 문서 — RED 세션 대화 |
| `report/02.UnitConvertor_TDD_RED_Report.md` | RED 단계 종합 보고서 |
| `.cursor/skills/unit-converter-tdd/reference.md` | D-*/U-* ID SSOT |
| `docs/PRD.md` | 요구사항·수용 기준 |
