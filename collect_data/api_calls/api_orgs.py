from common import github_api
from typing import Dict, List, Tuple


def create_org_values(json: Dict, CURRENT_TIME: str, org_name: str) -> Tuple:
    """
    organization api 요청 응답 값을 DB에 적재하기 알맞은 형태로 정제하는 함수입니다.

    Returns:
        dict
    """
    if json['name'] is None:  # name이 없을 경우 명시적으로 회사명 입력하기
        json['name'] = org_name

    return (
        json['id'],
        json['node_id'],
        json['name'],
        json['description'],
        json['company'],
        json['blog'],
        json['location'],
        json['email'],
        json['twitter_username'],
        json['followers'],
        json['following'],
        json['is_verified'],
        json['has_organization_projects'],
        json['has_repository_projects'],
        json['public_repos'],
        json['public_gists'],
        json['html_url'],
        json['avatar_url'],
        json['type'],
        json['created_at'],
        json['updated_at'],
        CURRENT_TIME
    )


def collect_api_orgs(HEADERS: Dict, ORGS: List[str], CURRENT_TIME) -> List[Tuple]:
    """
    위 모든 함수들을 종합하여 순차적으로 실행하는 함수로, organization 정보의 집합을 반환합니다.

    Args:
        ORGS (list) -> 정보를 가져올 조직 목록을 인자로 받습니다.

    Returns:
        list(tuple) -> 각 조직의 정보(tuple)를 리스트에 합쳐서 반환합니다.
    """
    data = []
    for org_name in ORGS:
        response = github_api(f'/orgs/{org_name}', HEADERS)
        json = response.json()
        org_values = create_org_values(json, CURRENT_TIME, org_name)
        data.append(org_values)
    return data
