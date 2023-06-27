from typing import Dict, List, Tuple
from common import github_api
import requests

# 필요 데이터 dict 변환


def create_repo_issue_values(json: Dict, CURRENT_TIME: str, repo_full_name: str) -> Tuple:
    """
    organization api 요청 응답 값을 DB에 적재하기 알맞은 형태로 정제하는 함수입니다.

    Returns:
        tuple
    """
    return (
        json['repository_url'],
        json['labels_url'],
        json['comments_url'],
        json['events_url'],
        json['html_url'],
        json['id'],
        json['node_id'],
        json['number'],
        json['title'],
        json['state'],
        json['locked'],
        json['comments'],
        json['created_at'],
        json['updated_at'],
        json['author_association'],
        json['body'],
        json['timeline_url'],
        json['state_reason'],
        json['user']['login'],
        CURRENT_TIME,
        repo_full_name
    )


def collect_api_repos_issues(HEADERS: Dict, repos: List, CURRENT_TIME) -> List[Tuple]:
    data = []
    params = {
        "per_page": 100,
    }

    for repo in repos:
        # pagenation
        params['page'] = 1
        params['state'] = 'all'
        params['filter'] = 'all'
        while True:
            try:
                response = github_api(f'/repos/{repo}/issues', HEADERS, params)
            except requests.exceptions.RequestException as e:
                print(f'Error: {e}')

            issues_json = response.json()
            if len(issues_json) == 0:
                break

            for issue_json in issues_json:
                data.append(create_repo_issue_values(
                    issue_json, CURRENT_TIME, repo))
            params['page'] += 1

    return data
