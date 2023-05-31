from yarl import URL
from collect_data.common import github_api

def clean_orgs_data(repo_content, CURRENT_TIME):
    """
    organization api 요청 응답 값을 DB에 적재하기 알맞은 형태로 정제하는 함수입니다.

    Returns:
        dict
    """
    return {
        'orgs_id': repo_content['id'],
        'node_id': repo_content['node_id'],
        'name': repo_content['name'],
        'description': repo_content['description'],
        'company': repo_content['company'],
        'blog': repo_content['blog'],
        'location': repo_content['location'],
        'email': repo_content['email'],
        'twitter_username': repo_content['twitter_username'],
        'followers': repo_content['followers'],
        'following': repo_content['following'],
        'is_verified': repo_content['is_verified'],
        'has_organization_projects': repo_content['has_organization_projects'],
        'has_repository_projects': repo_content['has_repository_projects'],
        'public_repos': repo_content['public_repos'],
        'public_gists': repo_content['public_gists'],
        'html_url': repo_content['html_url'],
        'avatar_url': repo_content['avatar_url'],
        'type': repo_content['type'],
        'created_at': repo_content['created_at'],
        'updated_at': repo_content['updated_at'],
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
        url = URL('https://api.github.com').with_path(f'orgs/{org_name}')
        json_data = github_api(url, HEADERS).json()
        values = clean_orgs_data(json_data, CURRENT_TIME)
        if values['name'] is None:  # name이 없을 경우 명시적으로 회사명 입력하기
            values['name'] = org_name
        data.append(values)
    return data
