from common import github_api
from typing import Dict, List, Tuple


def create_repo_languages_values(repo_fullname: str, language, usage_count, CURRENT_TIME) -> Tuple:
    return (
        repo_fullname,
        language,
        usage_count,
        CURRENT_TIME
    )


def collect_api_repos_languages(HEADERS: Dict, repos: List, CURRENT_TIME) -> List[Tuple]:
    data = []

    for repo_full_name in repos:
        response = github_api(f'/repos/{repo_full_name}/languages', HEADERS)
        repo_languages_json = response.json()
        for language, usage_count in repo_languages_json.items():
            data.append(create_repo_languages_values(
                repo_full_name, language, usage_count, CURRENT_TIME))

    return data
