import datetime
import os
import random
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

BATTLE_THRESHOLD = 2

def get_db_connection():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not found")
    
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)

def execute_sql(sql, error_message = None, fetchall = False, fetchone = False, params = None):
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not found")
    
    conn =  psycopg2.connect(database_url, cursor_factory=RealDictCursor)

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            
            result = None
            if fetchall:
                result = cursor.fetchall()
            elif fetchone:
                result = cursor.fetchone()
            # Don't fetch anything for INSERT/UPDATE/DELETE operations
            
            conn.commit()
            return result
    except Exception as e:
        print(f"{error_message}: {e}")
        return None

def count_squads():
    return execute_sql("SELECT COUNT(*) as squad_count FROM squads", "Error counting squads", fetchone = True)['squad_count']

def select_random_squads(count):
    return execute_sql("SELECT id, name FROM squads ORDER BY RANDOM() LIMIT %s", "Error selecting squads", fetchall = True, fetchone = False, params = (count,))
    
def get_squad_by_id(squad_id):
    return execute_sql("SELECT * FROM squads WHERE id = %s", "Error getting squad by id", fetchone = True, fetchall = False, params = (squad_id,))

def get_squad_units(squad_id):
    return execute_sql("SELECT * FROM units WHERE squad_id = %s", "Error getting squad units", fetchall = True, fetchone = False, params = (squad_id,))

def get_weapon_stats(weapon_name):
    return execute_sql("SELECT * FROM weapons WHERE name = %s", "Error getting weapon stats", fetchone = True, fetchall = False, params = (weapon_name,))

def get_armor_stats(armor_name):
    return execute_sql("SELECT * FROM armors WHERE name = %s", "Error getting armor stats", fetchone = True, fetchall = False, params = (armor_name,))

def get_race_stats(race_name):
    return execute_sql("SELECT * FROM races WHERE name = %s", "Error getting race stats", fetchone = True, fetchall = False, params = (race_name,))

def calculate_effective_speed(unit):
    weapon_stats = get_weapon_stats(unit['weapon'])
    armor_stats = get_armor_stats(unit['armor'])
    race_stats = get_race_stats(unit['race'])
    return race_stats['base_speed'] - (armor_stats['weight'] or 0)

def calculate_health(unit, current_health, damage_being_dealt):
    unit_race = get_race_stats(unit['race'])
    base_health = unit_race['base_hp']
    if current_health is None:
        current_health = base_health
    
    incoming_damage = damage_being_dealt
    if incoming_damage < 0:
        incoming_damage = 0
    
    remaining_health = current_health - incoming_damage
    if remaining_health < 0:
        remaining_health = 0
    return remaining_health

def battle(squads):
    
    squads_by_id = {squad['id']: squad for squad in squads}

    battle_report = []

    squad1_id = squads[0]['id']
    squad2_id = squads[1]['id']

    # Get the units for each squad.
    squad1_units = get_squad_units(squad1_id)
    squad2_units = get_squad_units(squad2_id)
    all_units = squad1_units + squad2_units

    for unit in all_units:
        unit['effective_speed'] = calculate_effective_speed(unit)
        unit['health'] = calculate_health(unit, None, 0)
        unit['attack_bonus'] = get_weapon_stats(unit['weapon'])['damage'] + get_race_stats(unit['race'])['base_damage']
        unit['defense_bonus'] = get_armor_stats(unit['armor'])['defense_bonus']

    # # Construct a list of all units' id, squad_id and effective speed.
    # turn_order = [
    #     {'id': unit['id'], 'squad_id': unit['squad_id'], 'effective_speed': unit['effective_speed']}
    #     for unit in all_units
    # ]
    
    # # Sort the units by effective speed.
    # turn_order.sort(key=lambda x: x['effective_speed'], reverse=True)

    units_by_id = {unit['id']: unit for unit in all_units}


    battle_report.append(f"{squads[0]['name']} and {squads[1]['name']} begin to fight!")

    # List each unit in each squad.
    battle_report.append(f"{squads[0]['name']} has {len(squad1_units)} units...")
    for unit in squad1_units:
        battle_report.append(f"{unit['name']} - {unit['race']} {unit['class']} (level {unit['level']}) wearing {unit['armor']} and wielding {unit['weapon']}")

    battle_report.append(f"{squads[1]['name']} has {len(squad2_units)} units...")
    for unit in squad2_units:
        battle_report.append(f"{unit['name']} - {unit['race']} {unit['class']} (level {unit['level']}) wearing {unit['armor']} and wielding {unit['weapon']}")

    battle_report.append("The battle begins!")

    while len(squad1_units) > 0 and len(squad2_units) > 0:
        # Update turn_order to only include alive units
        alive_units = [unit for unit in all_units if unit['health'] > 0]
        turn_order = [
            {'id': unit['id'], 'squad_id': unit['squad_id'], 'effective_speed': unit['effective_speed']}
            for unit in alive_units
        ]
        turn_order.sort(key=lambda x: x['effective_speed'], reverse=True)

        for unit in turn_order:
            current_unit_id = unit['id']
            current_unit_squad_id = unit['squad_id']
            current_unit_effective_speed = unit['effective_speed']

            current_unit = units_by_id[current_unit_id]
            current_squad = squads_by_id[current_unit_squad_id]

            # Set target_squad_id to the opposing squad.
            target_squad_id = squad2_id if current_unit_squad_id == squad1_id else squad1_id
            
            # Get all units from the opposing squad
            target_squad_units = [unit for unit in all_units if unit['squad_id'] == target_squad_id]
            target_squad_name = squads_by_id[target_squad_id]['name']

            # Only target units that are still alive
            alive_target_units = [unit for unit in target_squad_units if unit['health'] > 0]
            
            # Skip turn if no enemies are alive
            if not alive_target_units:
                battle_report.append(f"{current_unit['name']} of {current_squad['name']} has no enemies to attack!")
                continue
                
            target_unit = random.choice(alive_target_units)

            battle_report.append(f"{current_unit['name']} of {current_squad['name']} now attacks {target_unit['name']} of {target_squad_name}.")

            # Attack roll.
            attack_roll = random.randint(1, 20)
            battle_report.append(f"{current_unit['name']} rolls a {attack_roll} to attack {target_unit['name']}.")

            # Defense roll.
            defense_roll = random.randint(1, 20)
            battle_report.append(f"{target_unit['name']} rolls a {defense_roll} to defend against {current_unit['name']}.")

            attack_total = attack_roll + current_unit['attack_bonus']
            defense_total = defense_roll + target_unit['defense_bonus']

            damage_being_dealt = attack_total
            target_unit['health'] = calculate_health(target_unit, target_unit['health'], damage_being_dealt)
            battle_report.append(f"{target_unit['name']} of {target_squad_name} now has {target_unit['health']} health remaining.")

            if target_unit['health'] <= 0:
                # Remove from the original squad lists
                if target_unit['squad_id'] == squad1_id:
                    squad1_units.remove(target_unit)
                else:
                    squad2_units.remove(target_unit)
                battle_report.append(f"{target_unit['name']} of {target_squad_name} has been defeated!")

        # Check for victory after each round
        if len(squad1_units) == 0:
            winner_squad_id = squad2_id
            loser_squad_id = squad1_id
            break
        elif len(squad2_units) == 0:
            winner_squad_id = squad1_id
            loser_squad_id = squad2_id
            break

    battle_report.append("The battle is over!")

    return battle_report, winner_squad_id, loser_squad_id

def main():
    print("Checking number of squads...")
    
    # Count squads
    squad_count = count_squads()
    print(f"Squad count: {squad_count}")

    # Check if enough squads for a battle.
    if squad_count >= BATTLE_THRESHOLD:
        print("Beginning battle...")
        
        # Select 2 random squads to battle.
        squads = select_random_squads(2)

        # Begin the battle.
        battle_report, winner_squad_id, loser_squad_id = battle(squads)

        # Add the battle report to the reports folder.
        os.makedirs('reports', exist_ok=True)
        
        # Put the battle report in a file, line by line.
        with open(f'reports/battle_report_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as file:
            for line in battle_report:
                file.write(line + '\n')
        
        print("Battle report saved to reports folder.")
        

        print(f"The winner is {execute_sql('SELECT name FROM squads WHERE id = %s', 'Error getting winner name', fetchone = True, fetchall = False, params = (winner_squad_id,))['name']}!")
        print(f"The loser is {execute_sql('SELECT name FROM squads WHERE id = %s', 'Error getting loser name', fetchone = True, fetchall = False, params = (loser_squad_id,))['name']}!")
        # Drop the losing squad from the database.
        execute_sql("DELETE FROM squads WHERE id = %s", "Error dropping losing squad", fetchone = False, fetchall = False, params = (loser_squad_id,))

    print("Ending.")

if __name__ == "__main__":
    main()
