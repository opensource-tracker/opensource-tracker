from common import github_api
from typing import Dict

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


# 모든 이슈 받아서 data로 반환
def collect_api_repos_issues(HEADERS, CURRENT_TIME, repos):
    """
    위 모든 함수들을 종합하여 순차적으로 실행하는 함수로, organization 정보의 집합을 반환합니다.

    Args:
        ORGS (list) -> 정보를 가져올 조직 목록을 인자로 받습니다.

    Returns:
        list(dict) -> 각 조직의 정보(dict)를 리스트에 합쳐서 반환합니다.
    """
    cnt = 0
    data = []
    for repo in repos:
        response = github_api(f'/repos/{repo}/issues', HEADERS)
        jsons = response.json()
        try:
            for json in jsons:
                values = create_repo_issue_dict(json, CURRENT_TIME, repo)
                data.append(values)
                cnt += 1
                print(cnt)
        except Exception as e:
            # Handle the error here
            print(f"Error occurred while parsing JSON: {e}")
            continue
    print(data[0])
    return data

