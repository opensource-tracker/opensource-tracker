import requests
import os
import psycopg2
from dotenv import load_dotenv


def get_next_url(link_header):
    """
    This func returns the next url from Link Header.
    """

    links = link_header.split(',')

    for link in links:
        parts = link.split(';')

        if len(parts) == 2 and 'rel="next"' in parts[1]:
            url = parts[0].strip('<>')
            return url

    return None


def save_info_to_commits_table(
        sha,
        node_id,
        commit_author_name,
        commit_author_email,
        commit_author_date,
        commit_committer_name,
        commit_committer_email,
        commit_committer_date,
        commit_message,
        author_login,
        author_id,
        author_node_id,
        author_site_admin,
        committer_login,
        committer_id,
        committer_node_id,
        committer_site_admin,
        repo_full_name
):
    """
    This func saves info to 'api_repos_commits' table.
    """

    load_dotenv() # .env file load. in playground folder
    
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    database = os.environ.get('DB_DATABASE')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')

    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO adhoc.api_repos_commits (
            sha,
            node_id,
            commit_author_name,
            commit_author_email,
            commit_author_date,
            commit_committer_name,
            commit_committer_email,
            commit_committer_date,
            commit_message,
            author_login,
            author_id,
            author_node_id,
            author_site_admin,
            committer_login,
            committer_id,
            committer_node_id,
            committer_site_admin,
            repo_full_name,
            called_at
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, NOW()
            )
    """, (
        sha,
        node_id,
        commit_author_name,
        commit_author_email,
        commit_author_date,
        commit_committer_name,
        commit_committer_email,
        commit_committer_date,
        commit_message,
        author_login,
        author_id,
        author_node_id,
        author_site_admin,
        committer_login,
        committer_id,
        committer_node_id,
        committer_site_admin,
        repo_full_name
    ))

    try:
        conn.commit()
    
    except Exception as e:
        print(f"DB Commit Error: {str(e)}")
        conn.rollback()

    finally:
        cur.close()
        conn.close()

    return


def collect_api_repos_commits(repo_full_name):
    """
    This func gets info of commits from repos.
    Because GitHub API provides limited commits list (upto 30), so it used the pagenation.
    """

    load_dotenv() # .env file load. in playground folder
    access_token = os.environ.get('ACCESS_TOKEN')

    url = f'https://api.github.com/repos/{repo_full_name}/commits?per_page=100'

    headers = {'Authorization': f'token {access_token}'}

    commits = []
    page = 1

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            current_commits = response.json()
            commits.extend(current_commits)

            # In 'Link' header, get next page's URL
            link_header = response.headers.get('Link', '')
            next_url = get_next_url(link_header)

            if next_url:
                url = next_url
                page += 1
            else:
                break

        else:
            print(f"Response Status Error: {response.status_code}")
            return

    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    database = os.environ.get('DB_DATABASE')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')

    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    cur = conn.cursor()
    cur.execute("SELECT sha FROM adhoc.api_repos_commits WHERE repo_full_name = %s", (repo_full_name,))
    result = cur.fetchall()
    saved_sha_set = {row[0] for row in result}

    cur.close()
    conn.close()


    for commit in commits:
        sha = commit['sha']

        if sha in saved_sha_set:
            continue

        node_id = commit['node_id']

        commit_author_name = commit['commit']['author']['name']
        commit_author_email = commit['commit']['author']['email']
        commit_author_date = commit['commit']['author']['date']

        commit_committer_name = commit['commit']['committer']['name']
        commit_committer_email = commit['commit']['committer']['email']
        commit_committer_date = commit['commit']['committer']['date']
        commit_message = commit['commit']['message']

        author_login = None
        author_id = None
        author_node_id = None
        author_site_admin = None
        if 'author' in commit and commit['author'] is not None:
            if 'login' in commit['author']:
                author_login = commit['author']['login']
            if 'id' in commit['author']:
                author_id = commit['author']['id']
            if 'node_id' in commit['author']:
                author_node_id = commit['author']['node_id']
            if 'site_admin' in commit['author']:
                author_site_admin = commit['author']['site_admin']

        committer_login = None
        committer_id = None
        committer_node_id = None
        committer_site_admin = None
        if 'committer' in commit and commit['committer'] is not None:
            if 'login' in commit['committer']:
                committer_login = commit['committer']['login']
            if 'id' in commit['committer']:
                committer_id = commit['committer']['id']
            if 'node_id' in commit['committer']:
                committer_node_id = commit['committer']['node_id']
            if 'site_admin' in commit['committer']:
                committer_site_admin = commit['committer']['site_admin']

        save_info_to_commits_table(
            sha,
            node_id,
            commit_author_name,
            commit_author_email,
            commit_author_date,
            commit_committer_name,
            commit_committer_email,
            commit_committer_date,
            commit_message,
            author_login,
            author_id,
            author_node_id,
            author_site_admin,
            committer_login,
            committer_id,
            committer_node_id,
            committer_site_admin,
            repo_full_name
        )
        

    total_commits_count = len(commits)
    print(f"Total commits: {total_commits_count}")

    return


if __name__ == '__main__':
    repo_full_name = 'nhn/gameanvil.sample-game-client-unity'
    collect_api_repos_commits(repo_full_name)
