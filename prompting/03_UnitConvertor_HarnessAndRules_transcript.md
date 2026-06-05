# UnitConverter_24 — Harness·Cursor Rules 세션 Export Transcript

| 항목 | 내용 |
|------|------|
| 날짜 | 2026-06-05 |
| 세션 | pytest Harness 골격 + `.cursorrules` 초안 + transcript export |
| 선행 Transcript | `prompting/02_UnitConvertor_ProblemDefinition_transcript.md` |
| 참조 PRD | `docs/PRD.md` v0.2 (§7 Test Loop, §8.1 TC 매트릭스, M1; v0.2에서 IS-7~9 In Scope) |
| Agent 세션 ID | `2a8d745d-aeb6-40ad-a2ca-7f64d19805ff` |

---

## 세션 범위

- **In**: Test Loop용 **Harness 골격만** (구현·assert 본문 없음), 루트 **`.cursorrules` 40~80줄 초안**
- **Out**: `UnitConverter.py` 리팩터, TC assert 본문, git commit, README 수정

---

## 대화 본문

### Turn 1 — 최소 Harness 요청

**사용자:** 최소 Harness를 만들어줘. 코드·테스트 본문은 아직 작성하지 마. Harness 골격만.

**에이전트:** `docs/PRD.md` §8.1·`prompting/02` 다음 세션 제안(Test Loop Red)을 확인한 뒤 pytest Harness만 추가.

**산출 파일:**

| 파일 | 역할 |
|------|------|
| `pytest.ini` | `testpaths=tests`, `pythonpath=.`, markers `prd_s1`~`prd_s3` |
| `requirements-dev.txt` | `pytest>=8.0` |
| `tests/__init__.py` | 패키지 |
| `tests/inputs.py` | PRD §8.1 입력 상수 4개 |
| `tests/conftest.py` | `prd_inputs`, `supported_units` fixture 골격 |
| `tests/test_validation.py` | S1 슬롯 3개 (형식 / unknown / 숫자) |
| `tests/test_conversion.py` | S2 슬롯 1개 (`meter:2.5`) |

**TC 슬롯 ↔ PRD §8.1:**

| 테스트 함수 | 입력 (`tests/inputs.py`) |
|-------------|--------------------------|
| `test_meter_value_converts_to_all_supported_units` | `INPUT_VALID` = `meter:2.5` |
| `test_rejects_missing_colon_format` | `INPUT_BAD_FORMAT` = `meter` |
| `test_rejects_unknown_unit` | `INPUT_UNKNOWN_UNIT` = `inch:1` |
| `test_rejects_non_numeric_value` | `INPUT_BAD_NUMBER` = `meter:abc` |

**검증 명령·결과:**

```bash
pip install -r requirements-dev.txt
pytest
```

- `pytest --collect-only`: **4 tests collected**
- `pytest -q`: **4 skipped** (각 `@pytest.mark.skip(reason="Harness skeleton — Test Loop Red")`)

**에이전트 요약:** `UnitConverter.py`·README는 미수정. Red 단계에서 skip 제거 후 assert·캡처 fixture 작성 예고.

---

### Turn 2 — `.cursorrules` 초안 요청

**사용자:** UnitConvertor_24 루트에 `.cursorrules` 초안을 새로 만들어줘. (현재 없음)

- 도메인: 길이 단위 변환 CLI, 입력 `meter:2.5`, 출력 `2.5 meter = 8.2021 feet`(등록된 모든 단위)
- TDD: RED→GREEN→REFACTOR, assert 완화·skip·xfail 금지, MagicConstant SSOT (리터럴 산재 금지)
- AI: 한국어, TDD 시 Phase/Layer/Track 선언, git commit은 사용자 요청 시만
- 40~80줄, **다른 파일은 만들지 마**

**에이전트:** 루트에 `.cursorrules` **45줄**만 생성.

**주요 섹션:** 도메인 · 설계(OCP/SRP/registry) · MagicConstant/SSOT · TDD(Test Loop) · AI 선언(Phase/Layer/Track) · AI 행동 · 금지·주의

**에이전트 안내:** Cursor가 `.cursorrules`를 자동 로드하지 않으면 Settings → Rules 또는 `.cursor/rules` 이전 가능.

---

### Turn 3 — transcript export (본 문서)

**사용자:** prompting 폴더 아래 지금까지 대화 저장해줘.

**에이전트:** `prompting/03_UnitConvertor_HarnessAndRules_transcript.md` 저장 (본 파일).

---

## 세션 산출 요약

### Harness 디렉터리 구조

```text
UnitConverter_24/
├── pytest.ini
├── requirements-dev.txt
├── .cursorrules
└── tests/
    ├── __init__.py
    ├── inputs.py
    ├── conftest.py
    ├── test_validation.py
    └── test_conversion.py
```

### `.cursorrules`와 Harness 간 정합 (후속 작업)

| 항목 | Harness 현재 상태 | `.cursorrules` 요구 |
|------|-------------------|---------------------|
| TC 실행 | 4건 **skip** | skip **금지** |
| Test Loop | 골격(슬롯) | **RED**에서 실패하는 assert 먼저 |
| 계수 | `UnitConverter.py`에 `3.28084` 등 산재 | registry **SSOT** |

→ 다음 작업: **Phase RED**, **Layer Test Loop** — skip 제거, 실패 assert 추가, (이후 GREEN) registry·구현.

---

## 체크리스트

| 항목 | 완료 |
|------|------|
| pytest.ini + requirements-dev.txt | ✅ |
| tests/ 4 TC 슬롯 + inputs.py | ✅ |
| conftest fixture 골격 | ✅ |
| pytest collect 4 / run 4 skipped | ✅ |
| `.cursorrules` 45줄 (루트만) | ✅ |
| Export Transcript (본 문서) | ✅ |
| UnitConverter.py 변경 | ❌ (의도적 미수정) |
| TC assert 본문 (RED) | ❌ (다음 세션) |

---

## 문서 맵 (갱신)

```text
prompting/01_UnitConvertor_MomTest_transcript.md
prompting/02_UnitConvertor_ProblemDefinition_transcript.md
prompting/03_UnitConvertor_HarnessAndRules_transcript.md   ← 본 Export
report/01.UnitConvertor_ProblemDefinition_Report.md
docs/PRD.md
.cursorrules
pytest.ini
tests/
```

---

## 다음 세션 제안 (참고)

1. **RED** (`Track: S1-validation`): `test_validation.py` skip 제거, 형식·unknown·숫자 assert
2. **RED** (`Track: S2-conversion`): `test_conversion.py` skip 제거, `meter:2.5` 수치/출력 assert
3. **GREEN** (`Track: S3-registry`): registry SSOT + `UnitConverter.py` 최소 연동
4. `.cursorrules`의 skip 금지와 정합 — Harness의 임시 skip **제거가 선행 조건**
