CREATE TABLE adhoc.api_licenses (
  key         VARCHAR(255) NOT NULL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  spdx_id     VARCHAR(255) NOT NULL,
  node_id     VARCHAR(255) NOT NULL,
  url         TEXT,
  body        TEXT,
  permissions VARCHAR(100)[],
  conditions  VARCHAR(100)[],
  limitations VARCHAR(100)[],
  called_at   TIMESTAMP NOT NULL
);
