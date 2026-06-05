# TDD REFACTOR — 구조 정리·동작 유지

UnitConverter_24 **Dual-Track TDD** — **REFACTOR 단계만**. RED·GREEN·테스트 assert 추가·동작 변경은 이 커맨드 범위 밖.

참고: `.cursorrules`, `docs/PRD.md`, 테스트 ID — `.cursor/skills/unit-converter-tdd/reference.md`

---

## 필수 선언 (응답 첫 줄)

```
Phase: refactor | Layer: <domain|infrastructure|application|cli> | Track: <Logic|UI>
```

- **Logic Track:** `src/application/` · `src/domain/` · `src/infrastructure/` — SRP·SSOT·registry 정리
- **UI Track:** `src/cli.py` · `application/formatting/` — orchestration·출력만; 계수·단위 분기 금지

**전제:** 관련 pytest **전부 green**. REFACTOR 중 RED로 돌아가면 즉시 중단하고 원인 보고.

**Golden Master (REFACTOR 직전·최초 1회):** 현재 green 출력·변환·에러 메시지를 `tests/golden/`에 고정한다.

```bash
python scripts/capture_golden_masters.py
pytest tests/test_golden_master.py -q
```

의도적 동작 변경 후에는 캡처 스크립트로 golden만 재생성한다 (assert 완화 금지).

---

## 절차

1. **선언** — `Phase: REFACTOR` · Track · Layer. 이번에 정리할 파일·모듈 범위를 명시.
2. **Golden Master** — `tests/golden/`·`manifest.json` 존재 확인; 없으면 `capture_golden_masters.py` 실행 후 `test_golden_master.py` green.
3. **전제 확인** — 대상 Track scoped pytest → **전부 PASSED** 확인. FAIL이 있으면 REFACTOR 중단(GREEN 또는 버그 수정 먼저).
4. **목표** — SRP·SSOT·중복 제거·이름 정리. **동작 변경 없음** (변경이 필요하면 TC를 먼저 RED로 추가·수정).
5. **허용 변경**
   - 파일 분리·모듈 추출
   - registry 추출·`config/units.json` SSOT 정렬
   - cli 슬림화·application으로 로직 이동
   - import 경로·함수명 정리 (공개 API 시그니처 유지)
6. **금지** — assert 완화·테스트 삭제; FR-4~6 선행(M2 미완 시); RED/GREEN 범위 작업.
7. **실행**
   - 1차: 변경 직후 Track scoped pytest
   - 2차: **`pytest -q`** 전체 Test Loop
   - 필요 시 마커별: `pytest -m prd_s1 -q` · `pytest -m prd_s2 -q` · `pytest -m prd_s3 -q`
8. **보고** — 아래 보고 섹션 형식. 구조 변경 요약·diff 핵심·회귀 결과.

---

## pytest 예시 (bash)

```bash
# 의존성 (최초 1회)
pip install -r requirements-dev.txt

# Golden Master (REFACTOR 직전·회귀)
pytest tests/test_golden_master.py -q

# REFACTOR — Track 단위 (변경 직후)
pytest tests/domain/ -q
pytest tests/infrastructure/ -q
pytest tests/application/ -q
pytest tests/test_cli.py -q

# REFACTOR·PR 전 — 전체 Test Loop (필수)
pytest -q

# 마커 (S1/S2/S3 회귀)
pytest -m prd_s1 -q
pytest -m prd_s2 -q
pytest -m prd_s3 -q
```

**전체 green 유지**가 REFACTOR 완료 조건. 하나라도 FAIL이면 롤백 또는 GREEN 수준 수정 후 재시도.

---

## 보고

| 항목 | 내용 |
|------|------|
| **Track / Layer** | Logic \| UI · domain \| infrastructure \| application \| cli |
| **구조 변경 요약** | 분리·이동·추출한 모듈·역할 1~3줄 |
| **diff 핵심** | 파일 이동·registry·cli 슬림화 등 핵심 diff |
| **변경 파일** | `src/` (테스트는 동작 변경 시에만, 사유 명시) |
| **pytest 명령** | Track scoped · 전체 · 마커별 실행 명령 |
| **결과** | passed N · failed N · skipped N (skipped > 0이면 사유) |
| **SSOT** | `config/units.json` + registry 단일 출처 유지 여부 |
| **다음** | 다음 REFACTOR 항목 또는 다음 D-*/U-* RED |

---

## 금지

| 금지 | 이유 |
|------|------|
| **동작 변경** (리팩터 중 기능 추가·수정) | 동작 변경은 RED→GREEN 선행 |
| assert 완화·테스트 삭제 | 요구사항 퇴행 |
| **FR-4~6 선행** (M2 미완 시) | PRD 마일스톤 순서 |
| RED (assert 추가) · GREEN (최소 구현) | 별도 커맨드 |
| cli에 변환 계수·단위 분기 하드코딩 | SSOT·OCP 위반 |
| **domain에 파싱 로직** | 파싱은 application (PRD §5.0) |
| REFACTOR 중 pytest FAIL 무시 | 구조 변경이 회귀를 만들면 REFACTOR 실패 |

---

**완료 조건:** 구조·이름·중복만 정리했고, **`pytest -q` 전체 green**, 동작·공개 API 의미 **변경 없음**, SSOT·레이어 규칙 **유지**일 것.
