from typing import Dict
from common import github_api
import requests

# 필요 데이터 dict 변환
def create_repo_issue_dict(json: Dict, CURRENT_TIME:str, repo_full_name:str):
    """
    organization api 요청 응답 값을 DB에 적재하기 알맞은 형태로 정제하는 함수입니다.

    Returns:
        dict
    """
    return {
        'repository_url':json['repository_url'],
        'labels_url': json['labels_url'],
        'comments_url': json['comments_url'],
        'events_url': json['events_url'],
        'html_url': json['html_url'],
        'issues_id': json['id'],
        'node_id': json['node_id'],
        'number': json['number'],
        'title': json['title'],
        'state': json['state'],
        'locked': json['locked'],
        'comments': json['comments'],
        'created_at': json['created_at'],
        'updated_at': json['updated_at'],
        'author_association': json['author_association'],
        'body': json['body'],
        'timeline_url': json['timeline_url'],
        'state_reason': json['state_reason'],
        'login_user': json['user']['login'],
        'called_at' : CURRENT_TIME,
        'repo_full_name': repo_full_name 
    }



def collect_api_repos_issues(HEADERS, repos, CURRENT_TIME):
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
            response = github_api(f'/repos/{repo}/issues', HEADERS, params)
            if response.status_code != 200:
                print('API 요청이 실패하였습니다.')
                print('응답 상태 코드:', response.status_code)
                break

            issues_json = response.json()
            if len(issues_json) == 0:
                break

            for issue_json in issues_json:
                data.append(create_repo_issue_dict(issue_json, CURRENT_TIME, repo))
            params['page'] += 1

    return data
