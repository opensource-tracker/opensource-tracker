CREATE ROLE analytics_author;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw_data TO analytics_author;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA adhoc TO analytics_author;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO analytics_author;
