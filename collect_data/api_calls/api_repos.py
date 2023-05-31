from common import github_api
from typing import Dict, List


def create_repo_dict(json: Dict, CURRENT_TIME):
    return {
        'repo_id': json['id'],
        'node_id': json['node_id'],
        'owner_id': json['owner']['id'],
        'name': json['name'],
        'full_name': json['full_name'],
        'description': json['description'],
        'private': json['private'],
        'html_url': json['html_url'],
        'url': json['url'],
        'homepage': json['homepage'],
        'fork': json['fork'],
        'created_at': json['created_at'],
        'updated_at': json['updated_at'],
        'pushed_at': json['pushed_at'],
        'called_at': CURRENT_TIME,
        'size': json['size'],
        'stargazers_count': json['stargazers_count'],
        'forks_count': json['forks_count'],
        'open_issues_count': json['open_issues_count'],
        'language': json['language'],
        'archived': json['archived'],
        'disabled': json['disabled'],
        'license': json['license']['name'] if json['license'] else None,
        'allow_forking': json['allow_forking']
    }

def collect_api_repos(HEADERS: Dict, ORGS: List, CURRENT_TIME) -> List[Dict]:
    data = []

    for org in ORGS:
        response = github_api(f'/orgs/{org}/repos', HEADERS)
        repos_json = response.json()
        for repo_json in repos_json:
            data.append(create_repo_dict(repo_json, CURRENT_TIME))

    return data
