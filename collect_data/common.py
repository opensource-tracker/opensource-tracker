from typing import Dict, Optional
import requests

def github_api(uri: str, headers: Dict, params:Optional[Dict] = None) -> requests.Response:
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
        data = github_api('/repos/owner/repo', headers).json()
    """
    url = f'https://api.github.com{uri}'
    if params:
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        raise ValueError(f'{uri} Not Found')
    else:
        raise Exception(f'Something goes wrong with {uri}, status code: {response.status_code}')
