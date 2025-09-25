import datetime
import random
from db_utils import execute_sql, execute_transaction_with_results

# Battle system constants
BATTLE_THRESHOLD = 2
SQUADS_PER_BATTLE = 2 # I have no idea what would happen if this were to be changed.
DICE_MAX_VALUE = 20
LEVEL_INCREMENT = 1

def count_squads():
    return execute_sql("SELECT COUNT(*) as squad_count FROM squads", fetch_one=True)['squad_count']

def select_random_squads(count):
    return execute_sql("SELECT id, name FROM squads ORDER BY RANDOM() LIMIT %s", fetch_all=True, params=(count,))
    
def get_squad_units(squad_id):
    return execute_sql("SELECT * FROM units WHERE squad_id = %s", fetch_all=True, params=(squad_id,))

def get_weapon_stats(weapon_name):
    return execute_sql("SELECT * FROM weapons WHERE name = %s", fetch_one=True, params=(weapon_name,))

def get_armor_stats(armor_name):
    return execute_sql("SELECT * FROM armors WHERE name = %s", fetch_one=True, params=(armor_name,))

def get_race_stats(race_name):
    return execute_sql("SELECT * FROM races WHERE name = %s", fetch_one=True, params=(race_name,))

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
    
    # Initialize winner/loser variables
    winner_squad_id = None
    loser_squad_id = None

    # Get the units for each squad.
    squad1_units = get_squad_units(squad1_id)
    squad2_units = get_squad_units(squad2_id)
    all_units = squad1_units + squad2_units

    for unit in all_units:
        unit['effective_speed'] = calculate_effective_speed(unit)
        unit['health'] = calculate_health(unit, None, 0)
        unit['attack_bonus'] = get_weapon_stats(unit['weapon'])['damage'] + get_race_stats(unit['race'])['base_damage']
        unit['defense_bonus'] = get_armor_stats(unit['armor'])['defense_bonus']
        print(unit)

    

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
        battle_report.append(f"{unit['name']} - {unit['race']} wearing {unit['armor']} and wielding {unit['weapon']}")

    battle_report.append(f"{squads[1]['name']} has {len(squad2_units)} units...")
    for unit in squad2_units:
        battle_report.append(f"{unit['name']} - {unit['race']} wearing {unit['armor']} and wielding {unit['weapon']}")

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
            attack_roll = random.randint(1, DICE_MAX_VALUE)
            battle_report.append(f"{current_unit['name']} rolls a {attack_roll} to attack {target_unit['name']}.")

            # Defense roll.
            defense_roll = random.randint(1, DICE_MAX_VALUE)
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

    # Safety check - ensure we have valid winner/loser
    if winner_squad_id is None or loser_squad_id is None:
        battle_report.append("ERROR: Battle ended without a clear winner!")
        print("ERROR: Battle ended without a clear winner!")
        # Default to first squad as winner if something went wrong
        winner_squad_id = squad1_id
        loser_squad_id = squad2_id

    return battle_report, winner_squad_id, loser_squad_id

def complete_battle_atomically(winner_squad_id, loser_squad_id, battle_report_content, battle_timestamp):
    """
    Complete a battle by storing the report, leveling up the winner, and deleting the loser atomically.
    Either all operations succeed, or none do.
    
    Args:
        winner_squad_id: ID of the winning squad
        loser_squad_id: ID of the losing squad
        battle_report_content: The battle report text
        battle_timestamp: When the battle occurred
    
    Returns:
        True if successful, False if failed
    """
    # Prepare all operations for the transaction
    operations = [
        # 1. Insert battle report
        ("INSERT INTO battle_reports (winner_squad_id, loser_squad_id, report_content, battle_timestamp) VALUES (%s, %s, %s, %s)", 
         (winner_squad_id, loser_squad_id, battle_report_content, battle_timestamp)),
        
        # 2. Level up the winning squad
        ("UPDATE squads SET level = level + %s WHERE id = %s", 
         (LEVEL_INCREMENT, winner_squad_id)),
        
        # 3. Delete the losing squad (this will cascade delete all units)
        ("DELETE FROM squads WHERE id = %s", 
         (loser_squad_id,))
    ]
    
    # Execute the transaction
    results = execute_transaction_with_results(operations, "Failed to complete battle atomically")
    
    if results is None:
        return False
    
    return True

def main():
    print("Checking number of squads...")
    
    # Count squads
    squad_count = count_squads()
    print(f"Squad count: {squad_count}")

    # Check if enough squads for a battle.
    if squad_count >= BATTLE_THRESHOLD:
        print("Beginning battle...")
        
        # Select random squads to battle.
        squads = select_random_squads(SQUADS_PER_BATTLE)

        # Begin the battle.
        battle_report, winner_squad_id, loser_squad_id = battle(squads)

        # Get winner and loser names BEFORE the atomic transaction
        winner_name = execute_sql('SELECT name FROM squads WHERE id = %s', fetch_one=True, params=(winner_squad_id,))['name']
        loser_name = execute_sql('SELECT name FROM squads WHERE id = %s', fetch_one=True, params=(loser_squad_id,))['name']
        
        # Complete the battle atomically
        battle_timestamp = datetime.datetime.now()
        report_content = '\n'.join(battle_report)
        
        success = complete_battle_atomically(winner_squad_id, loser_squad_id, report_content, battle_timestamp)
        
        if not success:
            print("ERROR: Failed to complete battle atomically!")
            return
        
        print(f"Battle completed successfully!")
        print(f"The winner is {winner_name}!")
        print(f"The loser {loser_name} has been eliminated!")
        
        # Get the new level for confirmation
        new_level_result = execute_sql("SELECT level FROM squads WHERE id = %s", fetch_one=True, params=(winner_squad_id,))
        new_level = new_level_result['level'] if new_level_result else 'unknown'
        print(f"{winner_name} leveled up to level {new_level}!")

    print("Ending.")

if __name__ == "__main__":
    main()
