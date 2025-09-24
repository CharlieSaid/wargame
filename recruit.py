import datetime
import os
import random
from db_utils import execute_sql

# Recruitment system constants
RECRUIT_THRESHOLD = 20
MAX_SQUADS = 5000
UNITS_PER_SQUAD = 4

def count_squads():
    return execute_sql("SELECT COUNT(*) as squad_count FROM squads", fetch_one=True)['squad_count']

def get_all_races():
    return execute_sql("SELECT name FROM races", fetch_all=True)

def get_all_classes():
    return execute_sql("SELECT name FROM classes", fetch_all=True)

def get_all_armors():
    return execute_sql("SELECT name FROM armors", fetch_all=True)

def get_all_weapons():
    return execute_sql("SELECT name FROM weapons", fetch_all=True)

def create_squad(name, commander, description):
    """Create a new squad and return its ID"""
    return execute_sql(
        "INSERT INTO squads (name, commander, description) VALUES (%s, %s, %s) RETURNING id",
        fetch_one=True,
        params=(name, commander, description)
    )

def create_unit(squad_id, name, race, unit_class, armor, weapon):
    """Create a new unit for a squad"""
    return execute_sql(
        "INSERT INTO units (squad_id, name, race, class, armor, weapon) VALUES (%s, %s, %s, %s, %s, %s)",
        params=(squad_id, name, race, unit_class, armor, weapon)
    )

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
    """Generate a random squad with units"""
    print("Generating new squad...")
    
    # Generate squad details
    squad_name = generate_squad_name()
    commander = "System Recruiter"
    description = f"A generated squad created by the recruitment system on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Create the squad
    squad_result = create_squad(squad_name, commander, description)
    if not squad_result:
        print("Failed to create squad")
        return False
    
    squad_id = squad_result['id']
    print(f"Created squad: {squad_name} (ID: {squad_id})")
    
    # Get all available options for random selection
    races = [race['name'] for race in get_all_races()]
    classes = [cls['name'] for cls in get_all_classes()]
    armors = [armor['name'] for armor in get_all_armors()]
    weapons = [weapon['name'] for weapon in get_all_weapons()]
    
    # Generate random units for the squad
    num_units = UNITS_PER_SQUAD
    print(f"Creating {num_units} units for the squad...")
    
    for i in range(num_units):
        unit_name = generate_unit_name()
        race = random.choice(races)
        unit_class = random.choice(classes)
        armor = random.choice(armors)
        weapon = random.choice(weapons)
        
        # Create the unit
        create_unit(squad_id, unit_name, race, unit_class, armor, weapon)
        print(f"  Created unit: {unit_name} - {race} {unit_class} wearing {armor} and wielding {weapon}")
    
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
