import requests
from typing import List, Dict

def get_json(uri: str, headers: Dict) -> Dict:
    """
    uri를 기반으로 GitHub API를 보내고 JSON 응답을 dict로 반환합니다.

    Args:
        uri (str): 요청을 보내려는 URI
        headers (dict): HTTP 요청 헤더. 'Authorization'가 필요합니다.
    
    Returns:
        dict: 요청에 대한 JSON 응답
    
    Rasises:
        ValueError: API 실패 시
    
    Example:
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + <github_access_token>,
            'X-GitHub-Api-Version': '2022-11-28',
        }
        data = get_json('/repos/owner/repo', headers)
    """
    url = f'https://api.github.com{uri}'
    req = requests.get(url, headers=headers)
    if req.status_code != 200: # TODO: status_code에 맞게 Error 사용ㅓ
        raise ValueError
    else:
        return req.json()

def create_repo_license_dict(json: Dict, repo_full_name: str, current_time: str) -> Dict:
    return {
        'repo_full_name': repo_full_name,
        'license_key': json['license']['key'],
        'sha': json['sha'],
        'html_url': json['html_url'],
        'download_url': json['download_url'],
        'git_url': json['git_url'],
        'content': json['content'],
        'called_at': current_time
  }

def collect_api_repos_licenses(headers: Dict, repos: List[str], current_time: str) -> List[Dict]:
    """
    라이센스 키 목록을 받아 GitHub API를 활용하여 그 정보를 list[dict]로 반환합니다.

    Args:
        headers (dict): HTTP 요청 헤더. 'Authorization'가 필요합니다.    
        repos: ([str]): 레포 이름을 담은 배열. `owner/repo` 형식입니다.
        current_time: str: 현재 시각에 대한 문자열 표현

    Returns:
        list[dict]: 조회한 dict를 리스트로 반환합니다.
    
    Rasises:
        ValueError: API 실패 시
    
    Example:
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': 'Bearer ' + <github_access_token>,
            'X-GitHub-Api-Version': '2022-11-28',
        }
        collect_api_licenses(headers, ['unlicense'], current_datetime)
    """
    data = []
    for repo in repos:
        json = get_json(f'/repos/{repo}/license', headers)
        license_dict = create_repo_license_dict(json, repo, current_time)
        data.append(license_dict)
    return data
