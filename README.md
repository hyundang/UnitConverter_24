
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 프로젝트 구조
```text
config/
  units.json               # 단위·비율 SSOT (FR-6)
src/
  cli.py                   # CLI 진입점 (README 실행)
  application/
    parsing.py             # (권장) unit:value · 등록 문법 파싱
    use_cases.py           # 유스케이스 오케스트레이션
  domain/                  # 검증 · 변환 · registry
  infrastructure/          # config/units.json 로드
tests/
  test_cli.py
  application/             # 파싱 · use case TC (S1 형식·숫자 등)
  domain/                  # 검증 · 변환 TC (S1 unknown · S2)
  infrastructure/
```

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 비활성화
deactivate
```

프로젝트 **루트 디렉터리**에서 아래처럼 실행합니다. 입력은 **표준 입력(stdin)** 으로 전달합니다.

### 사용 방법

#### 1. 단위 변환 (기본)

입력 형식: `단위:숫자`

```bash
# Windows (PowerShell)
"meter:2.5" | python src/cli.py

# macOS / Linux
echo "meter:2.5" | python src/cli.py
```

출력 예 (기본 표 형식):

```text
+-------+-------+--------+
| unit  | input | value  |
+-------+-------+--------+
| meter |   2.5 |    2.5 |
| feet  |   2.5 | 8.2021 |
| yard  |   2.5 | 2.7340 |
+-------+-------+--------+
```

- `unit`: 변환 대상 단위
- `input`: 입력한 숫자 (모든 행에 동일)
- `value`: 해당 단위로 변환한 결과

기본 지원 단위: `meter`, `feet`, `yard` (`config/units.json`에서 관리)

#### 2. 출력 형식 선택

`--format` 옵션으로 출력 형태를 바꿀 수 있습니다.

| 옵션 | 설명 |
|------|------|
| `table` | 격자 표 형식 (기본값, `unit` / `input` / `value`) |
| `json` | JSON 객체 |
| `csv` | CSV |

```bash
"meter:2.5" | python src/cli.py --format json
"meter:2.5" | python src/cli.py --format csv
```

#### 3. 새 단위 등록 (런타임)

등록 형식: `1 단위명 = 비율 meter`

여러 줄을 입력할 수 있습니다. 등록 줄(`=`)은 단위를 추가하고, 변환 줄(`:`)은 변환을 수행합니다.

```bash
# Windows (PowerShell)
@"
1 cubit = 0.4572 meter
cubit:2
"@ | python src/cli.py
```

#### 4. 오류 입력

잘못된 입력 시 stderr에 원인 메시지가 출력되고 종료 코드는 `1`입니다.

| 입력 예 | 메시지 |
|---------|--------|
| `meter` | `Invalid format. Expected unit:value` |
| `meter:abc` | `Invalid number: abc` |
| `inch:1` | `unknown unit: inch. Supported units: ...` |

### 기본 요구사항

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력


## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
