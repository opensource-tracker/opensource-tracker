from yarl import URL
import requests
import datetime
import os


HEADERS = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.environ.get("GITHUB_TOKEN")}',
    'X-GitHub-Api-Version': '2022-11-28'
}


def get_json(url):
    """
    url로 api 요청을 보내고, 응답값을 json 형태로 반환하는 함수입니다.

    Args:
        url (str): 요청을 보낼 url 주소

    Returns:
        dict or list(dict)
    """
    req = requests.get(url, headers=HEADERS)
    return req.json()


def get_current_time():
    """
    현재 시간과 날짜를 문자열 형태로 반환하는 함수입니다.

    Returns:
        str -> 2023-05-30 18:42:24
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")


def clean_orgs_data(repo_content):
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
        'called_at': get_current_time()
    }


def collect_api_orgs(ORGS):
    """
    위 모든 함수들을 종합하여 순차적으로 실행하는 함수로, organization 정보의 집합을 반환합니다.

    Returns:
        list(dict) -> 각 조직의 정보(dict)를 리스트에 합쳐서 반환합니다.
    """
    data = []
    for org_name in ORGS:
        url = URL('https://api.github.com').with_path(f'orgs/{org_name}')
        json_data = get_json(url)
        values = clean_orgs_data(json_data)
        if values['name'] is None:  # name이 없을 경우 명시적으로 회사명 입력하기
            values['name'] = org_name
        data.append(values)
    return data
