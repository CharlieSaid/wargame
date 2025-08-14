-- cleanup.sql
-- Drops all tables to start fresh
-- Run this BEFORE running schema.sql and data.sql

-- Drop tables in reverse dependency order (child tables first)
DROP TABLE IF EXISTS units CASCADE;
DROP TABLE IF EXISTS squads CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS weapons CASCADE;
DROP TABLE IF EXISTS armors CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS races CASCADE;

-- Drop any remaining indexes (in case they weren't cleaned up)
DROP INDEX IF EXISTS idx_squads_user_id;
DROP INDEX IF EXISTS idx_units_squad_id;
DROP INDEX IF EXISTS idx_units_race;
DROP INDEX IF EXISTS idx_units_class;
DROP INDEX IF EXISTS idx_units_armor;
DROP INDEX IF EXISTS idx_units_weapon;
DROP INDEX IF EXISTS idx_units_level;

-- Show confirmation
SELECT 'Database cleaned up successfully!' as status; 