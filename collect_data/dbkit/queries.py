API_ORGS_TABLE_INSERT_SQL = "INSERT INTO adhoc.api_orgs (orgs_id, node_id, name,\
    description, company, blog, location, email, twitter_username,\
    followers, following, is_verified, has_organization_projects, \
    has_repository_projects, public_repos, public_gists, html_url, \
    avatar_url, type, created_at, updated_at, called_at) \
    VALUES (%(orgs_id)s, %(node_id)s, %(name)s, %(description)s, \
    %(company)s, %(blog)s, %(location)s, %(email)s, %(twitter_username)s, \
    %(followers)s, %(following)s, %(is_verified)s, %(has_organization_projects)s,\
    %(has_repository_projects)s, %(public_repos)s, %(public_gists)s, %(html_url)s,\
    %(avatar_url)s, %(type)s, %(created_at)s, %(updated_at)s, %(called_at)s);"
