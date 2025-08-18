# Wargame

## Build Squads and Battle your Rivals

This is a simple wargame where you can build squads of units and battle other players.

### Geography System
Each user has the ability to fight the 2 users ranked above them and the 2 users ranked below them at will.  This represents the location of rival armies and their distance from each other.  Since the enemies ranked 2 away are geographically farther, attacking an enemy ranked 2 away from you includes a -1 morale boost.

.
-
0
-
.

### Roving System
Each user has an outpost they occupy and defend.  Users can spend loot to improve their outpost's defensive capabilites.  Outposts captured can be moved into as the user's new home outpost.  Outpost upgrades remain with each outpost even if you lose that outpost and someone else gains it.

### Combat Loop
When combat starts, each unit starts at a distance (100) from the enemy units.  Since defending units are always in a specific outpost, they are all the same distance from each other.

Each "Turn", every unit moves its speed to move into range.  For units with melee weapons, this means moving closer, while units with ranged weapons will likely move farther away if they can.

After moving, if the unit is within range to attack, they do.  If they are not, they get to move a second time within the Turn.

When a unit attacks:
 - A random number between 1 and 100 is generated, representing the attack swing.
 - That number is modified by the weapon's weight, and the race's agility stat.
 - If the final attack roll is higher than the enemy's evasion (armor weight and the race's agility stat), the attack hits.  Otherwise it misses and the attack is over.
 - When an attack hits, it deals damage equal to the weapon's damage plus the race's damage and any other modifiers (class/skills) minus the enemy's armor stat and any skill modifiers.
 - Dealt damage is recorded in a unit's temporary "HP" stat.

After every unit able to attack has attacked, there is a cleanup phase where any units which have been dealt more damage than their base HP die.  Note that this happens after all attacks (meaning that even if a unit is attacked by 5 enemies simultaneously, they have a chance to attack back before they die).

Each unit has a cooldown of several turns.


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
