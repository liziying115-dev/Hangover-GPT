-- Pour Decisions — Supabase schema
-- Run this in the Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- before running seed.sql.

-- -----------------------------------------------------------------------
-- Table
-- -----------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS recipes (
    id            TEXT        PRIMARY KEY,
    name          TEXT        NOT NULL,
    description   TEXT,
    difficulty    TEXT        CHECK (difficulty IN ('easy', 'medium', 'hard')),
    serving_size  INTEGER     NOT NULL DEFAULT 1,
    base_spirit   TEXT,
    flavor_tags   JSONB       NOT NULL DEFAULT '[]',
    ingredients   JSONB       NOT NULL DEFAULT '[]',
    steps         JSONB       NOT NULL DEFAULT '[]',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index to speed up base_spirit and flavor_tags filtering used by the
-- Browse page.
CREATE INDEX IF NOT EXISTS idx_recipes_base_spirit ON recipes (base_spirit);
CREATE INDEX IF NOT EXISTS idx_recipes_flavor_tags ON recipes USING GIN (flavor_tags);

-- -----------------------------------------------------------------------
-- Row Level Security
-- -----------------------------------------------------------------------

ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;

-- Allow anyone (including anonymous / unauthenticated requests via the
-- anon key) to read recipes. The app never writes to this table at runtime.
CREATE POLICY "Public read access"
    ON recipes
    FOR SELECT
    USING (true);
