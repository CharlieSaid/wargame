# Wargame

## Build Squads and Battle your Rivals

This is a simple wargame where you can build squads of units and battle other players.

The database schema is in `sql/schema.sql`.

## Dev Guide

psql <Neon connection string> to enter the PSQL database.

Inside PSQL:
 - use backslash for commands.
 - \i runs files ("\i schema.sql").
 - \q exits psql.
 - \l lists all databases.
 - \c connects to a database ("\c my_database").
 - \dt describes all tables.
 - \d describes a specified table ("\d users").
 - \? is help with psql commands.
 - \h is SQL help ("\h SELECT").

I have several sql files:
 - schema.sql: The table setup.
 - cleanup.sql: Drops all tables and indexes.  Basically deletes everything.
 - data.sql: Inserts starting data.
 - rebuild.sql: Runs cleanup.sql and then schema.sql.  Then runs data.sql.  This basically resets the database.  NOTE that it restores the data to whatever data.sql inserts.  Manually inserted data would get deleted.

Render:
Render is on a free tier, meaning that services get put on the back burner after 15 minutes.  If they are loaded in this state, there may be a minute of waiting first.

