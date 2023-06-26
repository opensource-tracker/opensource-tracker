from typing import List, Dict, Tuple
from common import github_api
import requests


def create_repo_commit_values(json: Dict, repo_full_name: str, current_time: str) -> Tuple:
    author_login = None
    author_id = None
    author_node_id = None
    author_site_admin = None
    if 'author' in json and json['author'] is not None:
        if 'login' in json['author']:
            author_login = json['author']['login']
        if 'id' in json['author']:
            author_id = json['author']['id']
        if 'node_id' in json['author']:
            author_node_id = json['author']['node_id']
        if 'site_admin' in json['author']:
            author_site_admin = json['author']['site_admin']

    committer_login = None
    committer_id = None
    committer_node_id = None
    committer_site_admin = None
    if 'committer' in json and json['committer'] is not None:
        if 'login' in json['committer']:
            committer_login = json['committer']['login']
        if 'id' in json['committer']:
            committer_id = json['committer']['id']
        if 'node_id' in json['committer']:
            committer_node_id = json['committer']['node_id']
        if 'site_admin' in json['committer']:
            committer_site_admin = json['committer']['site_admin']

    return (
        json['sha'],
        json['node_id'],
        json['commit']['author']['name'],
        json['commit']['author']['email'],
        json['commit']['author']['date'],
        json['commit']['committer']['name'],
        json['commit']['committer']['email'],
        json['commit']['committer']['date'],
        json['commit']['message'],
        author_login,
        author_id,
        author_node_id,
        author_site_admin,
        committer_login,
        committer_id,
        committer_node_id,
        committer_site_admin,
        repo_full_name,
        current_time
    )


def collect_api_repos_commits(headers: Dict, repos: List[str], current_time: str) -> List[Tuple]:
    """
    github_api 함수를 통해 받아온 response.json() 에 접근해 페이지네이션 하지 않고 최근 커밋을 30개 받아옵니다.
    모든 repo에서 조회한 commit tuple를 리스트로 반환합니다.
    """

    data = []

    for repo in repos:
        uri = f'/repos/{repo}/commits?per_page=30'

        try:
            response = github_api(uri, headers)
        except requests.exceptions.HTTPError as e:
            print(f'Error: {e}')
        else:
            current_commits = response.json()

        for commit in current_commits:
            commit_values = create_repo_commit_values(
                commit, repo, current_time)
            data.append(commit_values)

    return data
