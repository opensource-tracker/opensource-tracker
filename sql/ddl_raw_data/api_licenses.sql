CREATE TABLE raw_data.api_licenses (
  key         VARCHAR(255),
  name        VARCHAR(255),
  spdx_id     VARCHAR(255),
  node_id     VARCHAR(255),
  url         TEXT,
  body        TEXT,
  permissions VARCHAR(100)[],
  conditions  VARCHAR(100)[],
  limitations VARCHAR(100)[],
  called_at   TIMESTAMP
);
