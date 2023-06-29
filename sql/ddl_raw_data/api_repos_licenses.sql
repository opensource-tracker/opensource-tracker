CREATE TABLE raw_data.api_repos_licenses (
  repo_full_name VARCHAR(255),
  license_key    VARCHAR(255),
  sha            VARCHAR(50),
  html_url       TEXT,
  download_url   TEXT,
  git_url        TEXT,
  content        TEXT,
  called_at      TIMESTAMP
);
