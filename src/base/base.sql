-- author: long nguyen (nguyenhailong253@gmail.com)

-- create schema
CREATE SCHEMA IF NOT EXISTS name_entity;
CREATE SCHEMA IF NOT EXISTS news;

-- create gov_officials table
-- test table
CREATE TABLE IF NOT EXISTS name_entity.test_gov_officials(
  added_id    SERIAL,
  id          uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name        TEXT NOT NULL,
  title       TEXT NOT NULL,
  extra       JSONB,
  office_term TEXT, 
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- main table
CREATE TABLE IF NOT EXISTS name_entity.gov_officials AS 
TABLE name_entity.test_gov_officials 
WITH NO DATA;

-- create organizations table

-- create news table
-- test table
CREATE TABLE IF NOT EXISTS news.test_zingnews(
  added_id      SERIAL,
  id            uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  src_id        VARCHAR,
  article_type  VARCHAR,
  topic_id      VARCHAR,
  url           VARCHAR,
  img_src       VARCHAR,
  title         VARCHAR,
  publish_time  VARCHAR,
  publish_date  VARCHAR,
  category      VARCHAR,
  author        VARCHAR,
  article_body  TEXT,
  tags          VARCHAR,
  summary       TEXT,
  extra         JSONB,
  posted_at     TIMESTAMPTZ,  
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- main table
CREATE TABLE IF NOT EXISTS news.zingnews AS 
TABLE name_entity.test_gov_officials 
WITH NO DATA;

-- truncate tables
TRUNCATE TABLE name_entity.test_gov_officials RESTART IDENTITY;
TRUNCATE TABLE news.test_zingnews RESTART IDENTITY;

-- drop table
DROP TABLE IF EXISTS name_entity.test_gov_officials CASCADE;
DROP TABLE IF EXISTS news.test_zingnews CASCADE;

-- grant privileges
GRANT ALL PRIVILEGES ON SCHEMA news, name_entity TO bitko_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA news, name_entity TO bitko_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA news, name_entity TO bitko_admin;

-- create index
CREATE INDEX idx_src_id ON news.test_zingnews(src_id);
