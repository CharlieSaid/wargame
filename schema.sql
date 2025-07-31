-- schema.sql
-- PostgreSQL-specific schema for a wargame

-- Races table: Each race that a unit can be
CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    skill VARCHAR(50) NOT NULL,
    base_HP INTEGER DEFAULT 100,
    base_speed INTEGER DEFAULT 10,
    description VARCHAR(1000)
);

-- Classes table: Each class that a unit can be
-- skill is a label that determines special abilities
CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    skill VARCHAR(50) NOT NULL
);

-- Armors table: Each armor that a unit can use
-- defense_bonus is the amount that the armor reduces incoming damage by
-- weight is the amount of weight that the armor adds to the unit
CREATE TABLE armors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    defense_bonus INTEGER DEFAULT 0,
    weight INTEGER DEFAULT 0,
    description VARCHAR(1000)
);

-- Weapons table: Each weapon that a unit can use
-- damage is the amount of damage that the weapon deals
-- damage_type is the type of damage that the weapon deals
CREATE TABLE weapons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    damage INTEGER DEFAULT 0,
    damage_type VARCHAR(20),
    description VARCHAR(1000)
);

-- Users table: Stores information about users who own armies
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Armies table: Each army belongs to one user
CREATE TABLE armies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(1000)
);

-- Units table: Each unit belongs to one army
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    army_id INTEGER NOT NULL REFERENCES armies(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    race VARCHAR(50) REFERENCES races(name),
    class VARCHAR(50) NOT NULL REFERENCES classes(name),
    level INTEGER NOT NULL CHECK (level > 0 AND level <= 1000),
    armor VARCHAR(50) REFERENCES armors(name),
    weapon VARCHAR(50) REFERENCES weapons(name),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(1000)
);

-- PostgreSQL indexes for better query performance
CREATE INDEX idx_armies_user_id ON armies(user_id);
CREATE INDEX idx_units_army_id ON units(army_id);
CREATE INDEX idx_units_race ON units(race);
CREATE INDEX idx_units_class ON units(class);
CREATE INDEX idx_units_armor ON units(armor);
CREATE INDEX idx_units_weapon ON units(weapon);
CREATE INDEX idx_units_level ON units(level);

