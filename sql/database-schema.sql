-- ==========================================
-- Reefscape Scout Database
-- PostgreSQL
-- ==========================================

-- --------------------------
-- USERS
-- --------------------------
CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    username INTEGER UNIQUE NOT NULL,      -- Número da equipe do scouter
    password_hash TEXT NOT NULL,

    role VARCHAR(20) DEFAULT 'scouter',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------
-- AUTO SCOUT
-- --------------------------
CREATE TABLE auto_scout_reefscape (
    id SERIAL PRIMARY KEY,

    event_key VARCHAR(50) NOT NULL,
    match_key VARCHAR(50) NOT NULL,

    team_key VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,

    l1 INTEGER DEFAULT 0,
    l2 INTEGER DEFAULT 0,
    l3 INTEGER DEFAULT 0,
    l4 INTEGER DEFAULT 0,

    coral_misseds INTEGER DEFAULT 0,

    coral_precision DECIMAL(5,2) DEFAULT 0
        CHECK (coral_precision >= 0 AND coral_precision <= 100),

    algae_removed INTEGER DEFAULT 0,
    algae_net INTEGER DEFAULT 0,
    algae_processor INTEGER DEFAULT 0,

    region_scored JSONB,

    score INTEGER DEFAULT 0,

    startline BOOLEAN DEFAULT FALSE,

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_auto_match_team
        UNIQUE (event_key, match_key, team_key)
);

-- --------------------------
-- TELEOP SCOUT
-- --------------------------
CREATE TABLE teleop_scout_reefscape (
    id SERIAL PRIMARY KEY,

    event_key VARCHAR(50) NOT NULL,
    match_key VARCHAR(50) NOT NULL,

    team_key VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,

    l1 INTEGER DEFAULT 0,
    l2 INTEGER DEFAULT 0,
    l3 INTEGER DEFAULT 0,
    l4 INTEGER DEFAULT 0,

    coral_misseds INTEGER DEFAULT 0,

    coral_precision DECIMAL(5,2) DEFAULT 0
        CHECK (coral_precision >= 0 AND coral_precision <= 100),

    algae_removed INTEGER DEFAULT 0,
    algae_net INTEGER DEFAULT 0,
    algae_processor INTEGER DEFAULT 0,

    climb VARCHAR(30),

    collected_coral_floor BOOLEAN DEFAULT FALSE,
    collected_coral_station BOOLEAN DEFAULT FALSE,
    collected_algae_reef BOOLEAN DEFAULT FALSE,

    issues BOOLEAN DEFAULT FALSE,
    issues_notes TEXT,

    defended BOOLEAN DEFAULT FALSE,

    driver_rating INTEGER,

    score INTEGER DEFAULT 0,

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_teleop_match_team
        UNIQUE (event_key, match_key, team_key)
);

-- --------------------------
-- PIT SCOUT
-- --------------------------
CREATE TABLE pit_scout (
    id SERIAL PRIMARY KEY,

    team_key VARCHAR(50) UNIQUE NOT NULL,

    description TEXT,

    img_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);