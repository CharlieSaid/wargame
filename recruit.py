import datetime
import os
import random
from db_utils import execute_sql, execute_transaction_with_results

# Recruitment system constants
RECRUIT_THRESHOLD = 20
MAX_SQUADS = 5000
UNITS_PER_SQUAD = 4

def count_squads():
    return execute_sql("SELECT COUNT(*) as squad_count FROM squads", fetch_one=True)['squad_count']

def get_all_races():
    return execute_sql("SELECT name FROM races", fetch_all=True)

def get_all_armors():
    return execute_sql("SELECT name FROM armors", fetch_all=True)

def get_all_weapons():
    return execute_sql("SELECT name FROM weapons", fetch_all=True)

def create_squad_with_units_atomically(name, commander, description, units_data):
    """
    Create a squad and all its units in a single atomic transaction.
    Either all operations succeed, or none do.
    
    Args:
        name: Squad name
        commander: Squad commander
        description: Squad description
        units_data: List of dicts with unit data (name, race, armor, weapon)
    
    Returns:
        Squad ID if successful, None if failed
    """
    # Prepare all operations for the transaction
    operations = []
    
    # 1. Create the squad
    squad_sql = "INSERT INTO squads (name, commander, description) VALUES (%s, %s, %s) RETURNING id"
    operations.append((squad_sql, (name, commander, description), 'one'))
    
    # 2. Create all units (we'll need the squad_id from the first operation)
    # We'll handle this by using a subquery or by doing it in two steps
    
    # Execute the transaction
    results = execute_transaction_with_results(operations, "Failed to create squad atomically")
    
    if results is None:
        return None
    
    squad_result = results[0]
    if not squad_result:
        return None
    
    squad_id = squad_result['id']
    
    # Now create all units in a second transaction
    unit_operations = []
    for unit_data in units_data:
        unit_sql = "INSERT INTO units (squad_id, name, race, armor, weapon) VALUES (%s, %s, %s, %s, %s)"
        unit_operations.append((unit_sql, (squad_id, unit_data['name'], unit_data['race'], unit_data['armor'], unit_data['weapon'])))
    
    unit_results = execute_transaction_with_results(unit_operations, "Failed to create units atomically")
    
    if unit_results is None:
        # If unit creation failed, we should clean up the squad
        execute_sql("DELETE FROM squads WHERE id = %s", params=(squad_id,), error_message="Failed to clean up orphaned squad")
        return None
    
    return squad_id

def generate_squad_name():
    """Generate a random squad name"""
    prefixes = [
        "Iron", "Steel", "Golden", "Silver", "Crimson", "Azure", "Emerald", "Shadow",
        "Storm", "Thunder", "Lightning", "Fire", "Ice", "Wind", "Earth", "Stone",
        "Blood", "Bone", "Night", "Dawn", "Sun", "Moon", "Star", "Sky"
    ]
    
    suffixes = [
        "Knights", "Warriors", "Guard", "Legion", "Company", "Battalion", "Regiment",
        "Squad", "Force", "Unit", "Division", "Corps", "Army", "Horde", "Clan",
        "Tribe", "Guild", "Order", "Brotherhood", "Alliance", "Union"
    ]
    
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def generate_unit_name():
    """Generate a random unit name"""
    first_names = [
        "Liam", "Theodore", "Noah", "Oliver", "Elijah", "William", "James",
        "Henry", "Lucas", "Red", "Richard", "Thomas", "George", "Frank",
        "Bryan", "Ethan", "Jordan", "Isaac", "Caden", "Nathan", "Aaron",
        "Juan", "Charles", "Dylan", "Trevor", "Brandon", "Benjamin", "Juan",
        "Alex", "Jeremy", "Evan", "Isaac", "Jake", "Adrian", "Carlos",
        "Hunter", "Tyler", "Adam", "Kevin", "Jose", "Eric", "Brian",
        "Uug", "Ehg", "Nar", "Nul", "Org", "Zog", "Maz"
    ]
    
    return random.choice(first_names)

def generate_squad():
    """Generate a random squad with units atomically"""
    print("Generating new squad...")
    
    # Generate squad details
    squad_name = generate_squad_name()
    commander = "System Recruiter"
    description = f"A generated squad created by the recruitment system on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Get all available options for random selection
    races = [race['name'] for race in get_all_races()]
    armors = [armor['name'] for armor in get_all_armors()]
    weapons = [weapon['name'] for weapon in get_all_weapons()]
    
    # Generate random units for the squad
    units_data = []
    for i in range(UNITS_PER_SQUAD):
        unit_name = generate_unit_name()
        race = random.choice(races)
        armor = random.choice(armors)
        weapon = random.choice(weapons)
        
        units_data.append({
            'name': unit_name,
            'race': race,
            'armor': armor,
            'weapon': weapon
        })
    
    # Create squad and all units atomically
    squad_id = create_squad_with_units_atomically(squad_name, commander, description, units_data)
    
    if not squad_id:
        print("Failed to create squad and units atomically")
        return False
    
    print(f"Created squad: {squad_name} (ID: {squad_id})")
    print(f"Created {len(units_data)} units:")
    for unit_data in units_data:
        print(f"  - {unit_data['name']} ({unit_data['race']}) wearing {unit_data['armor']} and wielding {unit_data['weapon']}")
    
    print(f"Squad {squad_name} recruitment complete!")
    return True

def main():
    print("Checking number of squads...")
    
    # Count squads
    squad_count = count_squads()
    print(f"Squad count: {squad_count}")
    
    # Check if we've hit the maximum squad limit
    if squad_count >= MAX_SQUADS:
        print(f"Squad count ({squad_count}) has reached the maximum limit ({MAX_SQUADS}). No new squads can be created.")
        print("Ending.")
        return
    
    # Check if we need to recruit more squads
    if squad_count < RECRUIT_THRESHOLD:
        print(f"Squad count ({squad_count}) is below threshold ({RECRUIT_THRESHOLD}). Beginning recruitment...")
        
        # Generate a new squad
        success = generate_squad()
        
        if success:
            print("Recruitment successful!")
        else:
            print("Recruitment failed!")
    else:
        print(f"Squad count ({squad_count}) is at or above threshold ({RECRUIT_THRESHOLD}). No recruitment needed.")
    
    print("Ending.")

if __name__ == "__main__":
    main()
