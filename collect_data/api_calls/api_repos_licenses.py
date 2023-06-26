from typing import List, Dict, Tuple
from common import github_api


def create_repo_license_values(json: Dict, repo_full_name: str, current_time: str) -> Tuple:
    return (
        repo_full_name,
        json['license']['key'],
        json['sha'],
        json['html_url'],
        json['download_url'],
        json['git_url'],
        json['content'],
        current_time
    )


def collect_api_repos_licenses(headers: Dict, repos: List[str], current_time: str) -> List[Tuple]:
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
        try:
            response = github_api(f'/repos/{repo}/license', headers)
            json = response.json()
            license_values = create_repo_license_values(
                json, repo, current_time)
            data.append(license_values)
        except ValueError:
            print(f"There is no licenses on {repo}")
    return data
