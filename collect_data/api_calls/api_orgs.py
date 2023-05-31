from common import github_api
from typing import Dict

def create_org_dict(json: Dict, CURRENT_TIME:str):
    """
    organization api 요청 응답 값을 DB에 적재하기 알맞은 형태로 정제하는 함수입니다.

    Returns:
        dict
    """
    return {
        'orgs_id': json['id'],
        'node_id': json['node_id'],
        'name': json['name'],
        'description': json['description'],
        'company': json['company'],
        'blog': json['blog'],
        'location': json['location'],
        'email': json['email'],
        'twitter_username': json['twitter_username'],
        'followers': json['followers'],
        'following': json['following'],
        'is_verified': json['is_verified'],
        'has_organization_projects': json['has_organization_projects'],
        'has_repository_projects': json['has_repository_projects'],
        'public_repos': json['public_repos'],
        'public_gists': json['public_gists'],
        'html_url': json['html_url'],
        'avatar_url': json['avatar_url'],
        'type': json['type'],
        'created_at': json['created_at'],
        'updated_at': json['updated_at'],
        'called_at': CURRENT_TIME
    }


def collect_api_orgs(HEADERS, ORGS, CURRENT_TIME):
    """
    위 모든 함수들을 종합하여 순차적으로 실행하는 함수로, organization 정보의 집합을 반환합니다.

    Args:
        ORGS (list) -> 정보를 가져올 조직 목록을 인자로 받습니다.

    Returns:
        list(dict) -> 각 조직의 정보(dict)를 리스트에 합쳐서 반환합니다.
    """
    data = []
    for org_name in ORGS:
        response = github_api(f'/orgs/{org_name}', HEADERS)
        json = response.json()
        values = create_org_dict(json, CURRENT_TIME)
        if values['name'] is None:  # name이 없을 경우 명시적으로 회사명 입력하기
            values['name'] = org_name
        data.append(values)
    return data
