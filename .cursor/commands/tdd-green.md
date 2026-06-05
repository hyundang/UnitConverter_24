# TDD GREEN — 최소 구현으로 테스트 통과

UnitConverter_24 **Dual-Track TDD** — **GREEN 단계만**. RED·REFACTOR·테스트 assert 추가는 이 커맨드 범위 밖.

참고: `.cursorrules`, `docs/PRD.md`, 테스트 ID — `.cursor/skills/unit-converter-tdd/reference.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: green | Layer: <domain|infrastructure|application|cli> | Track: <Logic|UI> | ID: <D-** 또는 U-**>
```

- **Logic Track:** `src/application/`(파싱), `src/domain/`(검증·변환), `src/infrastructure/` — **domain Mock 금지**; 파싱은 application만
- **UI Track:** `src/cli.py` — orchestration·print만; 변환 로직·계수 리터럴 금지

**전제:** 해당 ID의 RED가 완료됐고, 대상 테스트가 **의도한 이유로 FAIL** 상태여야 한다.

---

## 절차

1. **선언** — `Phase: GREEN` · Track · Layer · 이번 사이클 `D-*` / `U-*` 1개(또는 사용자 지정 범위). RED에서 실패한 테스트 함수명을 명시.
2. **최소 구현** — 방금 RED에서 실패한 assert만 통과시키는 코드만 `src/`에 추가. 범위 밖 리팩터·선행 기능 **금지**.
3. **레이어 준수**
   - **Logic:** application(파싱) · domain(검증·변환) · infrastructure — domain에 `print`/`input`/파싱 로직 없음
   - **UI:** cli는 application API 호출·출력 포맷만; `if unit ==`·`3.28084` 등 다중 리터럴 **금지**
4. **실행**
   - 1차: Track scoped pytest → **해당 테스트 green** 확인
   - 2차: **회귀** — Logic이면 `tests/domain/`(필요 시 `tests/application/`, `tests/infrastructure/`); UI면 `tests/test_cli.py`; 마무리로 `pytest tests/ -q`
5. **OCP 점검** — 단위 추가가 `main()` 분기·다중 리터럴 없이 registry/`config/units.json`만으로 가능한 구조인지 확인. 위반 시 REFACTOR 예고만 보고(이번 GREEN에서 대규모 구조 변경 금지).
6. **skip 금지** — Harness 잔여 `@pytest.mark.skip`이 이번 ID 범위에 있으면 **제거**했는지 확인. skip > 0이면 GREEN 미완.
7. **보고** — 아래 보고 섹션 형식. 통과/실패 개수; 다음 REFACTOR 또는 다음 `D-*` / `U-*` ID.

---

## pytest 예시 (bash)

```bash
# 의존성 (최초 1회)
pip install -r requirements-dev.txt

# GREEN — 단일 테스트 (권장, RED와 동일 대상)
pytest tests/domain/test_validation.py::test_rejects_missing_colon_format -x -q
pytest tests/domain/test_conversion.py::test_meter_value_converts_to_all_supported_units -x -q
pytest tests/test_cli.py::test_<name> -x -q

# GREEN — Track 단위
pytest tests/domain/ -q
pytest tests/infrastructure/ -q
pytest tests/application/ -q
pytest tests/test_cli.py -q

# GREEN 완료 — 회귀
pytest tests/ -q

# 마커 (S1/S2 슬롯)
pytest -m prd_s1 -q
pytest -m prd_s2 -q
```

대상 테스트가 **PASSED**이고, 회귀에서 **unexpected FAIL 없음**일 때 GREEN 완료.

---

## 보고

| 항목 | 내용 |
|------|------|
| **테스트 ID** | D-** / U-** |
| **구현 요약** | 추가·수정한 `src/` Layer·핵심 동작 1~2줄 |
| **변경 파일** | `src/` (및 skip 제거한 `tests/` 경로) |
| **pytest 명령** | 1차 대상 테스트 · 2차 회귀 명령 |
| **결과** | passed N · failed N · (skipped > 0이면 GREEN 미완) |
| **OCP** | registry/설정만으로 확장 가능 여부 (OK / REFACTOR 필요) |
| **다음** | REFACTOR 항목 1줄 또는 다음 D-*/U-* ID |

---

## 금지

| 금지 | 이유 |
|------|------|
| RED 범위 작업 (assert 추가·완화·삭제) | 테스트 요구사항은 RED에서만 변경 |
| **REFACTOR** (구조 개편·이름 정리·중복 제거) | GREEN은 최소 통과만 — 별도 커맨드 |
| RED 실패와 무관한 기능·파일 대량 추가 | YAGNI — 해당 assert만 통과 |
| **Logic Track에서 domain Mock** | 실제 domain/application으로 검증 |
| **domain에 파싱 로직** | 파싱은 application (PRD §5.0) |
| cli에 변환 계수·단위 분기 하드코딩 | SSOT·OCP 위반 |
| `@pytest.mark.skip` · `xfail` 유지·추가 | Harness 우회 |
| assert 완화로 green 만들기 | 요구사항 퇴행 |

---

**완료 조건:** 선택한 ID의 대상 테스트 **PASSED**, 회귀 **unexpected FAIL 없음**, 해당 범위 **skip 0**, 변경이 **최소 구현**에 한정될 것.
