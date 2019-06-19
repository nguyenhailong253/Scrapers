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
  title         VARCHAR,
  summary       TEXT,
  article_body  TEXT,
  url           VARCHAR,
  publish_time  VARCHAR,
  publish_date  VARCHAR,
  category      VARCHAR,
  author        VARCHAR,
  author_url    VARCHAR,
  article_type  VARCHAR,
  topic_id      VARCHAR,
  like_count    SMALLINT,
  dislike_count SMALLINT,
  rating_count  SMALLINT,
  viral_count   SMALLINT,
  comment_count SMALLINT,
  img_src       VARCHAR,
  tags          VARCHAR,
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