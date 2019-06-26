-- author: long nguyen (nguyenhailong253@gmail.com)

-- create schema
CREATE SCHEMA IF NOT EXISTS gov_officials;
CREATE SCHEMA IF NOT EXISTS news;

-- create gov_officials table
-- test table
CREATE TABLE IF NOT EXISTS gov_officials.test_gov_officials(
  added_id    SERIAL,
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        TEXT NOT NULL,
  title       TEXT NOT NULL,
  extra       JSONB,
  office_term TEXT, 
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- main table
CREATE TABLE IF NOT EXISTS gov_officials.gov_officials AS 
TABLE gov_officials.test_gov_officials 
WITH NO DATA;

-- create organizations table

-- create news table
-- test table
CREATE TABLE IF NOT EXISTS news.test(
  added_id      SERIAL,
  src_id        VARCHAR,
  article_type  VARCHAR,
  url           VARCHAR,
  img_src       VARCHAR,
  title         VARCHAR,
  publish_time  VARCHAR,
  publish_date  VARCHAR,
  category      VARCHAR,
  author        VARCHAR,
  content_raw   VARCHAR,
  content_text  TEXT,
  tags_raw      VARCHAR,
  tags_text     TEXT,
  summary       TEXT,
  like_count    VARCHAR,
  dislike_count VARCHAR,
  rating_count  VARCHAR,
  viral_count   VARCHAR,
  comment_count VARCHAR,
  topic_id      VARCHAR,
  posted_at     TIMESTAMPTZ,  
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (src_id)
);

-- main table
CREATE TABLE IF NOT EXISTS news.zing AS 
TABLE news.test
WITH NO DATA;

-- truncate tables
TRUNCATE TABLE gov_officials.test_gov_officials RESTART IDENTITY;
TRUNCATE TABLE news.test_zingnews RESTART IDENTITY;

-- drop table
DROP TABLE IF EXISTS gov_officials.test_gov_officials CASCADE;
DROP TABLE IF EXISTS news.test_zingnews CASCADE;

-- grant privileges
GRANT ALL PRIVILEGES ON SCHEMA news, gov_officials TO bitko_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA news, gov_officials TO bitko_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA news, gov_officials TO bitko_admin;

-- create index
CREATE INDEX idx_src_id ON news.test_zingnews(src_id);
