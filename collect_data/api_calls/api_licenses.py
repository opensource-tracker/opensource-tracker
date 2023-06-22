from typing import List, Dict
from common import github_api

def create_license_dict(json: Dict, current_time: str) -> Dict:
    return {
        'key': json['key'],
        'name': json['name'],
        'spdx_id': json['spdx_id'],
        'node_id': json['node_id'],
        'url': json['url'],
        'body': json['body'],
        'permissions': json['permissions'],
        'conditions': json['conditions'],
        'limitations': json['limitations'],
        'called_at': current_time
    }

def collect_api_licenses(headers: Dict, licenses: List[str], current_time: str) -> List[Dict]:
    """
    라이센스 키 목록을 받아 GitHub API를 활용하여 그 정보를 list[dict]로 반환합니다.

    Args:
        headers (dict): HTTP 요청 헤더. 'Authorization'가 필요합니다.
        licenses: ([str]): 조회하고자 하는 라이센스 이름. license-key 형식입니다.
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
    for license in licenses:
        response = github_api(f'/licenses/{license}', headers)
        json = response.json()
        license_dict = create_license_dict(json, current_time)
        data.append(license_dict)
    return data
