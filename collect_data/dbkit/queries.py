API_ORGS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_orgs
(orgs_id, node_id, name, description, company, blog, location, email, twitter_username,
followers, following, is_verified, has_organization_projects, has_repository_projects,
public_repos, public_gists, html_url, avatar_url, type, created_at, updated_at, called_at)
VALUES
(%(orgs_id)s, %(node_id)s, %(name)s, %(description)s, %(company)s, %(blog)s, %(location)s,
%(email)s, %(twitter_username)s, %(followers)s, %(following)s, %(is_verified)s,
%(has_organization_projects)s, %(has_repository_projects)s, %(public_repos)s,
%(public_gists)s, %(html_url)s, %(avatar_url)s, %(type)s, %(created_at)s, %(updated_at)s,
%(called_at)s);
"""

API_LICENSES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_licenses
(key, name, spdx_id, node_id, url, body, permissions, conditions, limitations, called_at)
VALUES
(%(key)s, %(name)s, %(spdx_id)s, %(node_id)s, %(url)s, %(body)s,
%(permissions)s, %(conditions)s, %(limitations)s, %(called_at)s)
"""

API_REPOS_LICENSES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_licenses
(repo_full_name, license_key, sha, html_url, download_url, git_url, content, called_at)
VALUES
(%(repo_full_name)s, %(license_key)s, %(sha)s, %(html_url)s, %(download_url)s, %(git_url)s, %(content)s, %(called_at)s)
"""

API_REPOS_SELECT_FULL_NAME_SQL = """
SELECT DISTINCT full_name FROM adhoc.api_repos
"""

API_REPOS_ISSUES_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_issues
(repository_url, labels_url, comments_url, events_url, html_url, issues_id, node_id, number, title, state, locked, comments,
created_at, updated_at, author_association, body, timeline_url, state_reason, login_user, called_at, repo_full_name)
VALUES
(%(repository_url)s, %(labels_url)s, %(comments_url)s, %(events_url)s, %(html_url)s, %(issues_id)s, %(node_id)s,
%(number)s, %(title)s, %(state)s, %(locked)s, %(comments)s, %(created_at)s, %(updated_at)s, %(author_association)s, %(body)s,
%(timeline_url)s, %(state_reason)s, %(login_user)s, %(called_at)s, %(repo_full_name)s)
"""

API_REPOS_COMMITS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos_commits
(sha, node_id, commit_author_name, commit_author_email, commit_author_date,
commit_committer_name, commit_committer_email, commit_committer_date,
commit_message, author_login, author_id, author_node_id, author_site_admin,
committer_login, committer_id, committer_node_id, committer_site_admin,
repo_full_name, called_at)
VALUES
(%(sha)s, %(node_id)s, %(commit_author_name)s, %(commit_author_email)s,
%(commit_author_date)s, %(commit_committer_name)s, %(commit_committer_email)s,
%(commit_committer_date)s, %(commit_message)s, %(author_login)s, %(author_id)s,
%(author_node_id)s, %(author_site_admin)s, %(committer_login)s, %(committer_id)s,
%(committer_node_id)s, %(committer_site_admin)s, %(repo_full_name)s, %(called_at)s
"""

API_REPOS_TABLE_INSERT_SQL = """
INSERT INTO adhoc.api_repos (repo_id, node_id, owner_id, name, full_name, description, private, html_url, \
url, homepage, fork, created_at, updated_at, pushed_at, called_at, size, stargazers_count, forks_count, \
open_issues_count, language, archived, disabled, license, allow_forking)
VALUES
(%(repo_id)s, %(node_id)s, %(owner_id)s, %(name)s, %(full_name)s, %(description)s, %(private)s, %(html_url)s, \
%(url)s, %(homepage)s, %(fork)s, %(created_at)s, %(updated_at)s, %(pushed_at)s, %(called_at)s, %(size)s, \
%(stargazers_count)s, %(forks_count)s, %(open_issues_count)s, %(language)s, %(archived)s, %(disabled)s, %(license)s, \
%(allow_forking)s)
"""
