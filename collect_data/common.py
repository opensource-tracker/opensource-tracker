from typing import Dict
import requests

def github_api(uri: str, headers: Dict):
    """
    uri를 기반으로 GitHub API를 보내고 응답을 반환합니다.
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
        data = github_api('/repos/owner/repo', headers)
    """
    url = f'https://api.github.com{uri}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200: # TODO: status_code에 맞게 Error 사용ㅓ
        raise ValueError
    else:
        return response
