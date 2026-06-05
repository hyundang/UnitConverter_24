# D-* / U-* 테스트 ID (UnitConverter_24)

| ID | Track | PRD | 입력·조건 |
|----|-------|-----|-----------|
| D-01 | Logic | S2 · §8.1 | `meter:2.5` → meter/feet/yard 변환 |
| D-02 | Logic | S1 · §8.1 | `meter` → 형식 오류 |
| D-03 | Logic | S1 · §8.1 | `inch:1` → unknown unit + 힌트 |
| D-04 | Logic | S1 · §8.1 | `meter:abc` → 숫자 오류 |
| D-05 | Logic | FR-6 · §8.2 | `config/units.json` 로드·README 비율 |
| D-06 | Logic | FR-5 · §8.2 | `1 cubit = 0.4572 meter` 등록 후 `cubit:1` |
| D-07 | UI | FR-4 · §8.2 | `--format json` (또는 문서화 옵션) |
| D-08 | UI | FR-4 · §8.2 | `--format csv` |
| D-09 | UI | FR-4 · §8.2 | 기본 표 출력 (D-01 동등 수치) |
| D-10 | Logic | S3 · FR-3 | 단위 1개 추가 · diff 1파일 |
| U-01 | UI | §9.1 | `python src/cli.py` + `meter:2.5` 대화형 |
| U-02 | UI | S1 · §9.2 | 잘못된 형식 → 메시지·예시 |
| U-03 | UI | §9.6 | 동적 등록 CLI 흐름 |
| U-04 | UI | §9.7 | 포맷 옵션 end-to-end |

**pytest 매핑 (현재 Harness):** D-02~D-04 → `tests/domain/test_validation.py` · D-01 → `tests/domain/test_conversion.py`
