CREATE TABLE adhoc.api_repos_issuses_labels (
  id SERIAL PRIMARY KEY,
  issues_id INT NOT NULL,
  labels_id INT NOT NULL,
  labels_url TEXT,
  name VARCHAR(255),
  color VARCHAR(255),
  description TEXT,
  repo_full_name VARCHAR(255) NOT NULL
);

