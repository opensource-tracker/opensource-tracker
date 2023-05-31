CREATE TABLE adhoc.api_repos_licenses (
  repo_full_name VARCHAR(255) NOT NULL,
  license_key    VARCHAR(255),
  sha            VARCHAR(50) NOT NULL,
  html_url       TEXT NOT NULL,
  download_url   TEXT NOT NULL,
  git_url        TEXT NOT NULL,
  content        TEXT,
  called_at      TIMESTAMP NOT NULL
);
