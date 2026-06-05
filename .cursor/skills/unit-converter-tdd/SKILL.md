---
name: unit-converter-tdd
description: >-
  UnitConverter_24 Dual-Track TDD·OCP 개발 시 Agent가 따를 절차. Use when working on
  UnitConverter_24, src/cli.py, unit conversion, registry SSOT, pytest RED/GREEN/REFACTOR,
  단위 추가, Mom Test S1~S4, or PRD Test Loop.
---

# UnitConverter_24 — Dual-Track TDD Skill

`.cursorrules`, `docs/PRD.md` v0.2.1, `README.md`와 함께 사용한다. 테스트 ID는 [reference.md](reference.md).

## 언제 이 Skill을 켜는지

| 상황 | Skill 적용 |
|------|------------|
| `src/domain` · `infrastructure` · `application` 구현·리팩터 | **Logic Track** |
| `src/cli.py` · 출력 포맷 · stdin/argv · 사용자 메시지 | **UI Track** |
| `tests/`에 assert 추가·skip 제거·회귀 확인 | 해당 Track + Test Loop |
| 단위 추가·`config/units.json`·FR-4~6 (M4) | Logic 선행 후 UI; S3 diff 1파일 |
| 사용자가 RED / GREEN / REFACTOR / TDD 명시 | **필수** |
| Harness만 두고 skip 유지·assert 완화 요청 | **Skill과 충돌 — 거부** |

작업 시작 시 한 줄 선언: **Phase** · **Track** (Logic | UI) · **Layer** · **D-*/U-*** ID

---

## Logic Track vs UI Track

| 구분 | Logic Track | UI Track |
|------|-------------|----------|
| **목적** | 규칙·변환·SSOT·유스케이스 | 진입·I/O·포맷·메시지 표면 |
| **코드** | `src/domain/`, `src/infrastructure/`, `src/application/` | `src/cli.py`, `application/formatting/` (FR-4) |
| **SSOT** | `config/units.json` + registry (R2) | SSOT 읽기만; 계수 정의 금지 |
| **테스트** | `tests/domain/`, `tests/infrastructure/`, `tests/application/` | `tests/test_cli.py` |
| **PRD** | S1, S2, S3, FR-5, FR-6 | S1 메시지 노출, FR-4, §9.1 시나리오 |
| **의존** | domain ← infrastructure | cli → application → domain |
| **금지** | `print`/`input` in domain | `if unit ==`·`3.28084` 리터럴 in cli |

**Dual-Track 규칙:** Logic Track TC가 green이기 전에 UI Track에서 변환 로직을 새로 쓰지 않는다. UI는 application API를 호출만 한다.

---

## RED (5~7단계)

1. **선언:** `Phase: RED` · Track · Layer · 대상 `D-*` / `U-*` (reference.md).
2. **범위 고정:** 이번 사이클에 손댈 파일·테스트 파일만 나열 (최소 diff).
3. **테스트 먼저:** 해당 Track의 테스트에 **실패하는 assert** 작성; `@pytest.mark.skip`·`xfail`·`pass` **금지**.
4. **실행:** Track에 맞는 pytest (아래 Test/Review Loop) — **실패 확인** (실패 이유가 기대와 일치하는지).
5. **프로덕션:** Logic은 `src/domain` 등 **구현 없음** 또는 스텁만; UI RED는 cli 테스트만 실패시키는 최소 변경.
6. **SSOT:** 테스트·프로덕션이 동일 `config/units.json` / loader 경로를 쓰도록 설계 (테스트 전용 중복 상수 금지).
7. **보고:** 실패 테스트명·실패 메시지 요약; GREEN에서 할 일 1줄.

---

## GREEN (5~7단계)

1. **선언:** `Phase: GREEN` · Track · Layer · `D-*` / `U-*`.
2. **최소 구현:** 방금 RED에서 실패한 assert만 통과시키는 코드만 추가.
3. **레이어 준수:** Logic — domain/infrastructure/application; UI — cli는 orchestration·print만.
4. **실행:** Track scoped pytest → **해당 테스트 green**; 이어서 **회귀** (`tests/domain/` 또는 전체 `pytest`).
5. **OCP 점검:** 단위 추가가 `main()` 분기·다중 리터럴 없이 registry/설정만으로 가능한지.
6. **skip 금지:** Harness 잔여 skip이 있으면 이번 GREEN 범위에서 제거했는지 확인.
7. **보고:** 통과/실패 개수; 다음 REFACTOR 또는 다음 D-* ID.

---

## REFACTOR (5~7단계)

1. **선언:** `Phase: REFACTOR` · Track · Layer.
2. **전제:** 관련 pytest **전부 green** (REFACTOR 중 RED로 돌아가지 않음).
3. **목표:** SRP·SSOT·중복 제거·이름 정리; **동작 변경 없음** (변경 필요 시 TC 먼저 RED).
4. **허용 변경:** 파일 분리, registry 추출, cli 슬림화, application으로 로직 이동.
5. **금지:** assert 완화, 테스트 삭제, FR-4~6 선행(M2 미완 시).
6. **실행:** `pytest` 전체; 필요 시 `prd_s1` / `prd_s2` / `prd_s3` 마커별.
7. **보고:** 구조 변경 요약·diff 핵심·회귀 결과.

---

## Test / Review Loop — pytest 언제 돌리는지

| 시점 | 명령 | 목적 |
|------|------|------|
| RED 직후 | `pytest <대상 파일> -x -q` | 의도한 **실패** 1건 확인 |
| Logic 작업 중 | `pytest tests/domain/ -q` | S1·S2 슬롯 |
| infrastructure | `pytest tests/infrastructure/ -q` | D-05 (설정 로드) |
| application | `pytest tests/application/ -q` | use case |
| UI 작업 중 | `pytest tests/test_cli.py -q` | U-* |
| GREEN 완료 | `pytest tests/ -q` | Track 회귀 |
| REFACTOR·PR 전 | `pytest -q` | 전체 Test Loop |
| S1만 | `pytest -m prd_s1 -q` | 검증 TC |
| S2만 | `pytest -m prd_s2 -q` | 변환 TC |
| S3·registry | `pytest -m prd_s3 -q` | 단일 출처·확장 |

설치: `pip install -r requirements-dev.txt` · 설정: `pytest.ini` (`pythonpath = . src`).

**Review Loop (수동):** 전체 green 후 PRD §8 S1~S4 체크리스트와 reference.md ID 매핑을 대조한다.

---

## 완료 보고 항목

작업 단위 종료 시 **한국어**로 짧게 보고한다.

| # | 항목 |
|---|------|
| 1 | **Phase / Track / Layer / D-*/U-*** |
| 2 | 변경 파일 목록 |
| 3 | 실행한 pytest 명령 |
| 4 | 결과: passed / failed / skipped (skipped > 0이면 사유·다음 RED) |
| 5 | SSOT 준수 여부 (`config/units.json`, R2 위반 없음) |
| 6 | 남은 RED 항목 (reference.md ID) |
| 7 | git: commit/push 여부 (**사용자 요청 시에만**) |

---

## PRD·마일스톤 정렬

| 단계 | 내용 |
|------|------|
| M2 | D-01~D-04 Logic RED→GREEN (S1·S2) |
| M3 | D-10·S3 registry 1파일 diff |
| M4 | D-05→D-06→D-07~D-09 (IS-9→8→7), S4 |

Command 파일(슬래시 커맨드)은 본 Skill 범위 외 — 별도 추가 시 Rule·Command 문서와 동기화한다.
