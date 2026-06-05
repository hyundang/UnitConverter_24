# TDD RED — 실패 테스트 먼저

UnitConverter_24 **Dual-Track TDD** — **RED 단계만**. GREEN·REFACTOR·`src/` 구현은 이 커맨드 범위 밖.

참고: `.cursorrules`, `docs/PRD.md`, 테스트 ID — `.cursor/skills/unit-converter-tdd/reference.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: red | Layer: <domain|infrastructure|application|cli> | Track: <Logic|UI> | ID: <D-** 또는 U-**>
```

- **Logic Track:** `tests/domain/`, `tests/infrastructure/`, `tests/application/` — `src/domain` 등 **직접 import**, domain **Mock 금지**
- **UI Track:** `tests/test_cli.py` — subprocess `python src/cli.py` 또는 `cli` + `capsys`

---

## 절차

1. **ID 확인** — `reference.md`에서 이번 사이클 `D-*` / `U-*` 1개(또는 사용자 지정 범위) 선택. PRD §8.1·§8.2와 매핑 확인.
2. **대상 테스트 파일 확정** — Logic: `tests/domain/test_validation.py` · `test_conversion.py` 등 / UI: `tests/test_cli.py`. **변경은 `tests/` 아래만.**
3. **AAA 테스트 작성**
   - **Arrange:** `tests/inputs.py`, `conftest` fixture (`prd_inputs`, `supported_units`, `config/units.json` 경로)
   - **Act:** import한 domain/application API 또는 CLI 호출
   - **Assert:** 기대 실패·기대 값 — **명확하고 엄격**하게
4. **Harness 정리** — 해당 테스트의 `@pytest.mark.skip` **제거**. `xfail`·`pass`·assert 삭제 **금지**.
5. **pytest FAIL** — 아래 예시로 실행. **의도한 이유로 실패**했는지 확인 (ImportError만 나면 “미구현” 실패로 인정, GREEN 범위임을 보고).
6. **보고** — 아래 보고 섹션 형식.

---

## pytest 예시 (bash)

```bash
# 의존성 (최초 1회)
pip install -r requirements-dev.txt

# RED — 단일 테스트 (권장)
pytest tests/domain/test_validation.py::test_rejects_missing_colon_format -x -q
pytest tests/domain/test_conversion.py::test_meter_value_converts_to_all_supported_units -x -q
pytest tests/test_cli.py::test_<name> -x -q

# RED — Track 단위
pytest tests/domain/ -x -q
pytest tests/infrastructure/ -x -q
pytest tests/application/ -x -q
pytest tests/test_cli.py -x -q

# 마커 (S1/S2 슬롯)
pytest -m prd_s1 -x -q
pytest -m prd_s2 -x -q
```

실패가 **기대한 assertion/동작**과 일치할 때만 RED 완료. 전부 skip이면 RED 미완.

---

## 보고

| 항목 | 내용 |
|------|------|
| **테스트 ID** | D-** / U-** |
| **FAIL 요약** | 실패 테스트 함수명 · 핵심 assert/에러 1~2줄 |
| **변경 파일** | `tests/` 아래 경로만 나열 |
| **pytest 명령** | 실제 실행한 명령 |
| **결과** | failed N · (skipped 있으면 RED 미완으로 표시) |
| **다음** | GREEN에서 손댈 `src/` Layer 1줄 (구현 제안만, 코드 작성 없음) |

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | RED는 테스트만 — GREEN에서 구현 |
| **Logic Track에서 domain Mock** | domain 규칙은 실제 객체·fixture로 검증 |
| assert 완화·삭제 | 요구사항 퇴행 |
| `@pytest.mark.skip` · `xfail` | `.cursorrules` · Harness 우회 |
| `tests/` 밖 문서·설정 대량 수정 | RED 범위 이탈 |
| GREEN / REFACTOR 작업 | 별도 커맨드·요청 |

---

**완료 조건:** 선택한 ID에 대해 pytest가 **FAILED** (또는 domain 미구현 시 **ERROR/ImportError** — GREEN 예고)이고, 변경 diff가 **`tests/`만**일 것.
