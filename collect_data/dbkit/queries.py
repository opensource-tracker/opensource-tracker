API_ORGS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_orgs
(orgs_id, node_id, name, description, company, blog, location, email, twitter_username,
followers, following, is_verified, has_organization_projects, has_repository_projects,
public_repos, public_gists, html_url, avatar_url, type, created_at, updated_at, called_at)
VALUES %s;
"""

API_LICENSES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_licenses
(key, name, spdx_id, node_id, url, body, permissions, conditions, limitations, called_at)
VALUES %s;
"""

API_REPOS_LICENSES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_licenses
(repo_full_name, license_key, sha, html_url, download_url, git_url, content, called_at)
VALUES %s;
"""

API_REPOS_SELECT_FULL_NAME_SQL = """
SELECT DISTINCT full_name FROM adhoc.api_repos;
"""


API_REPOS_ISSUES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_issues
(repository_url, labels_url, comments_url, events_url, html_url, issues_id, node_id, number, title, state, locked,
comments, created_at, updated_at, author_association, body, timeline_url, state_reason, login_user, called_at,
repo_full_name)
VALUES %s;
"""


API_REPOS_COMMITS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_commits
(sha, node_id, commit_author_name, commit_author_email, commit_author_date,
commit_committer_name, commit_committer_email, commit_committer_date,
commit_message, author_login, author_id, author_node_id, author_site_admin,
committer_login, committer_id, committer_node_id, committer_site_admin,
repo_full_name, called_at)
VALUES %s;
"""

API_REPOS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos
(repo_id, node_id, owner_id, name, full_name, description, private, html_url,
url, homepage, fork, created_at, updated_at, pushed_at, called_at, size, stargazers_count, forks_count,
open_issues_count, language, archived, disabled, license, allow_forking)
VALUES %s;
"""

API_REPOS_LANGUAGES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_languages (repo_full_name, language, usage_count, called_at)
VALUES %s;
"""
