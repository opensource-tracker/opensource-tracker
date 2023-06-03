# Opensource tracker

[GitHub REST API](https://docs.github.com/ko/rest?apiVersion=v3)를 활용하여 국내 기업의 오픈소스 현황을 대시보드로 보여줍니다.

## Team

- 프로그래머스 데이터엔지니어링 데브코스 1기
- 2차 프로젝트 1팀 1조
- 기간: 2023. 05. 29. (월) ~ 06. 02. (금)

| **김민석** | **서대원** | **안수빈** | **이수영** | **정희원** |
|:---:|:---:|:---:|:---:|:---:|
| ![kmus1232](https://github.com/kmus1232.png) | ![DaewonSeo](https://github.com/DaewonSeo.png) | ![nyeong](https://github.com/nyeong.png) | ![jeslsy](https://github.com/jeslsy.png) | ![heewoneha](https://github.com/heewoneha.png) |


## Result of This Project

> ⭐ 대시보드에서 Organization과 Repository 이름에 대한 필터를 걸 수 있습니다.

### 1. For all organizations

![for all orgs](https://github.com/opensource-tracker/opensource-tracker/assets/74031620/ed9fcc85-6d20-4a5a-b5b4-70a43a10dc0e)

### 2. For each organization
![for each organization](https://github.com/opensource-tracker/opensource-tracker/assets/74031620/76d08f0f-ea1b-443d-aa05-5717bce57aa8)

### 3. For each repository
![for-each-repository](https://github.com/opensource-tracker/opensource-tracker/assets/74031620/a04eecaa-6a8a-45e1-819f-b04cc6888656)


## Tech Stack

| Field | Stack |
|:---:|:---|
| Language | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"/> |
| Data Base | <img src="https://img.shields.io/badge/Amazon RDS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>  |
| Dashboard | <img src="https://img.shields.io/badge/Preset-04B404?style=for-the-badge&logo=preset&logoColor=white"/> |
| Cron-job | <img src="https://img.shields.io/badge/github actions-181717?style=for-the-badge&logo=githubactions&logoColor=white"> |


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


## How did we create the dashboard

```mermaid
  flowchart LR;
      classDef green color:#022e1f,fill:#5FB404;
      classDef black color:#fff,fill:#2E2E2E;

      A["/orgs/{org_name}"]:::black--api_orgs-->B;
      C["/orgs/{org}/repos"]:::black--api_repos-->B;
      E["/orgs/{org}/repos/commits"]:::black--api_repos_commits-->B;
      F["/repos/{repo}/license"]:::black--api_repos_licenses-->B;
      G["/repos/{repo_full_name}/languages"]:::black--api_repos_languages-->B;
      H["/repos/{repo}/issues"]:::black--api_repos_issues-->B;
      I["/licenses/{license}"]:::black--api_licenses-->B;
      B[DB]--Get Data from AWS RDS-->D[Dashboard]:::green;
```
