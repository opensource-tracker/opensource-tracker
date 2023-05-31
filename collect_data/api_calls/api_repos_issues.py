from common import github_api
from typing import Dict
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

    for repo in repos:
        url = f'https://api.github.com/repos/{repo}/issues'
        issues = []
        params = {'page': 1}

        # pagenation
        while True:
            response = requests.get(url, params=params, headers=HEADERS)
            if response.status_code == 200:
                json_data = response.json()
                issues.extend(json_data)
                if 'next' in response.links:
                    url = response.links['next']['url']
                    params = {}
                else:
                    break
            else:
                print('Error:', response.status_code)
                break

        # 모든 issues를 dict 형태로 반환해서 data에 연속 저장
        try:
            for issue in issues:
                values = create_repo_issue_dict(issue, CURRENT_TIME, repo)
                data.append(values)
        except Exception as e:
            # Handle the error here
            print(f"Error occurred while parsing JSON: {e}")
    
    return data