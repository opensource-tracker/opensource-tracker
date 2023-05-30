# opensource tracker

국내 기업의 오픈소스 현황을 대시보드로 보여줍니다.

## Usage

```bash
# venv 활성화
$ . .venv/bin/activate

# 의존성 설치
$ pip install -r requirements.txt
```

## Structures

```
.
├── README.md
├── requirements.txt
├── .github/workflows/
├── collect_data/       데이터 수집을 위한 파이썬 코드
│  ├── collect_data.py
│  ├── api_calls/
│  └── playground/
└── sql/                SQL 정의
   ├── dcl/
   └── ddl_raw_data/
```
