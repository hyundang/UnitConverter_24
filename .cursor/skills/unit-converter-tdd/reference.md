# D-* / U-* 테스트 ID (UnitConverter_24)

| ID | Track | Layer | PRD | 입력·조건 |
|----|-------|-------|-----|-----------|
| D-01 | Logic | domain | S2 · §8.1 | `meter:2.5` → meter/feet/yard 변환 |
| D-02 | Logic | application | S1 · §8.1 | `meter` → 형식 오류 (파싱 실패) |
| D-03 | Logic | domain | S1 · §8.1 | `inch:1` → unknown unit + 힌트 (검증) |
| D-04 | Logic | application | S1 · §8.1 | `meter:abc` → 숫자 오류 (파싱 실패) |
| D-05 | Logic | infrastructure | FR-6 · §8.2 | `config/units.json` 로드·README 비율 |
| D-06 | Logic | application | FR-5 · §8.2 | `1 cubit = 0.4572 meter` 등록 파싱 후 `cubit:1` |
| D-07 | UI | cli | FR-4 · §8.2 | `--format json` |
| D-08 | UI | cli | FR-4 · §8.2 | `--format csv` |
| D-09 | UI | cli | FR-4 · §8.2 | 기본 표 출력 (D-01 동등) |
| D-10 | Logic | domain | S3 · FR-3 | 단위 1개 추가 · diff 1파일 |
| U-01 | UI | cli | §9.1 | `python src/cli.py` + `meter:2.5` |
| U-02 | UI | cli | S1 · §9.2 | 잘못된 형식 → 메시지·예시 |
| U-03 | UI | cli | §9.6 | 동적 등록 CLI |
| U-04 | UI | cli | §9.7 | 포맷 E2E |
