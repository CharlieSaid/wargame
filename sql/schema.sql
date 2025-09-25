-- schema.sql
-- PostgreSQL-specific schema for a wargame

-- Races table: Each race that a unit can be
CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    skill VARCHAR(50) NOT NULL,
    base_HP INTEGER DEFAULT 100,
    base_speed INTEGER DEFAULT 10,
    base_agility INTEGER DEFAULT 100, -- both accuracy of own attacks and evasion of enemy attacks
    base_damage INTEGER DEFAULT 10,  -- modifier to damage of own attacks
    description VARCHAR(1000)
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
    range INTEGER DEFAULT 0,
    description VARCHAR(1000)
);

-- Squads table: Anyone can create and view squads
-- commander is the name of the person who created the squad
-- level represents the squad's battle experience and ranking
CREATE TABLE squads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    commander VARCHAR(100),
    level INTEGER DEFAULT 1 CHECK (level >= 1),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(1000)
);

-- Units table: Each unit belongs to one squad
CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES squads(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    race VARCHAR(50) REFERENCES races(name),
    armor VARCHAR(50) REFERENCES armors(name),
    weapon VARCHAR(50) REFERENCES weapons(name),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(1000)
);

-- Battle Reports table: Store battle reports in database instead of files
CREATE TABLE battle_reports (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    winner_squad_id INTEGER REFERENCES squads(id),
    loser_squad_id INTEGER REFERENCES squads(id),
    report_content TEXT NOT NULL,
    battle_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- PostgreSQL indexes for better query performance
CREATE INDEX idx_units_squad_id ON units(squad_id);
CREATE INDEX idx_units_race ON units(race);
CREATE INDEX idx_units_armor ON units(armor);
CREATE INDEX idx_units_weapon ON units(weapon);
CREATE INDEX idx_squads_level ON squads(level);
CREATE INDEX idx_squads_created_at ON squads(created_at);
CREATE INDEX idx_battle_reports_created_at ON battle_reports(created_at);
CREATE INDEX idx_battle_reports_winner ON battle_reports(winner_squad_id);
CREATE INDEX idx_battle_reports_loser ON battle_reports(loser_squad_id);

