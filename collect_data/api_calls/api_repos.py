from common import github_api
from typing import Dict, List, Tuple


def create_repo_values(json: Dict, current_time) -> Tuple:
    return (
        json['id'],
        json['node_id'],
        json['owner']['id'],
        json['name'],
        json['full_name'],
        json['description'],
        json['private'],
        json['html_url'],
        json['url'],
        json['homepage'],
        json['fork'],
        json['created_at'],
        json['updated_at'],
        json['pushed_at'],
        current_time,
        json['size'],
        json['stargazers_count'],
        json['forks_count'],
        json['open_issues_count'],
        json['language'],
        json['archived'],
        json['disabled'],
        json['license']['name'] if json['license'] else None,
        json['allow_forking']
    )


def collect_api_repos(headers: Dict, orgs: List, current_time) -> List[Tuple]:
    data = []
    params = {
        "per_page": 100,
    }

    for org in orgs:
        params['page'] = 1
        while True:
            response = github_api(f'/orgs/{org}/repos', headers, params)
            repos_json: List = response.json()
            if len(repos_json) == 0:
                break
            for repo_json in repos_json:
                data.append(create_repo_values(repo_json, current_time))
            params['page'] += 1

    return data
