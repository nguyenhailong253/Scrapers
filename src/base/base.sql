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


-- truncate tables
TRUNCATE TABLE name_entity.test_gov_officials RESTART IDENTITY;