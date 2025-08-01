-- rebuild.sql
-- Master script to completely rebuild the database
-- This runs cleanup, schema, and data in the correct order

\echo 'Starting database rebuild...'

-- Step 1: Clean up existing tables
\i cleanup.sql

\echo 'Cleanup complete. Creating new schema...'

-- Step 2: Create fresh schema
\i schema.sql

\echo 'Schema created. Inserting sample data...'

-- Step 3: Insert sample data
\i data.sql

\echo 'Database rebuild complete!'
\echo 'You can now query your tables:'
\echo 'SELECT * FROM races;'
\echo 'SELECT * FROM classes;'
\echo 'SELECT * FROM armors;'
\echo 'SELECT * FROM weapons;' 