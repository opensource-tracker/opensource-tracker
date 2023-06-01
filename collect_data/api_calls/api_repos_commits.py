from typing import List, Dict
from common import github_api

def create_repo_commit_dict(json: Dict, repo_full_name: str, current_time: str) -> Dict:
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

    return {
        'sha': json['sha'],
        'node_id': json['node_id'],
        'commit_author_name': json['commit']['author']['name'],
        'commit_author_email': json['commit']['author']['email'],
        'commit_author_date': json['commit']['author']['date'],
        'commit_committer_name': json['commit']['committer']['name'],
        'commit_committer_email': json['commit']['committer']['email'],
        'commit_committer_date': json['commit']['committer']['date'],
        'commit_message': json['commit']['message'],
        'author_login': author_login,
        'author_id': author_id,
        'author_node_id': author_node_id,
        'author_site_admin': author_site_admin,
        'committer_login': committer_login,
        'committer_id': committer_id,
        'committer_node_id': committer_node_id,
        'committer_site_admin': committer_site_admin,
        'repo_full_name': repo_full_name,
        'called_at': current_time
    }


def collect_api_repos_commits(headers: Dict, repos: List[str], current_time: str) -> List[Dict]:
    """
    github_api 함수를 통해 받아온 response.json() 에 접근해 페이지네이션 하지 않고 최근 커밋을 30개 받아옵니다.
    모든 repo에서 조회한 commit dicts를 리스트로 반환합니다.
    """

    data = []

    for repo in repos:
        commits = []
        url = f'https://api.github.com/repos/{repo}/commits?per_page=30'
        
        uri = url.split('https://api.github.com')[1]
        response = github_api(uri, headers)

        current_commits = response.json()
        commits.extend(current_commits)
        
        for commit in commits:
            commit_dict = create_repo_commit_dict(commit, repo, current_time)
            data.append(commit_dict)
    
    return data
