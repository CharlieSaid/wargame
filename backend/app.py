"""
WARGAME BACKEND API
A simple Flask API for managing squads and units in a medieval wargame.
No user system - anyone can create and view squads.
"""

import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# ============================
# CONFIGURATION & SETUP
# ============================

class Config:
    """Load environment variables and configuration"""
    def __init__(self):
        load_dotenv()
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.DEBUG = os.getenv("FLASK_DEBUG", True)

config = Config()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://charliesaid.github.io"}})

# ============================
# DATABASE UTILITIES
# ============================

def get_db_connection():
    """Create a new database connection with RealDictCursor for JSON-friendly results"""
    return psycopg2.connect(config.DATABASE_URL, cursor_factory=RealDictCursor)

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query with proper connection management
    
    Args:
        query: SQL query string
        params: Query parameters tuple
        fetch_one: Return single row
        fetch_all: Return all rows
    
    Returns:
        Query result or number of affected rows
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
    except psycopg2.IntegrityError as e:
        raise ValueError("Data constraint violation") from e
    except Exception as e:
        raise RuntimeError(f"Database error: {str(e)}") from e

# ============================
# VALIDATION & ERROR HANDLING
# ============================

def validate_required_fields(data, required_fields):
    """Check that all required fields are present in the request"""
    if not data:
        return "Request body is required"
    
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return f"Missing required fields: {', '.join(missing)}"
    return None

def handle_error(error):
    """Convert Python exceptions to appropriate HTTP responses"""
    if isinstance(error, ValueError):
        return jsonify({"error": str(error)}), 400
    elif isinstance(error, RuntimeError):
        return jsonify({"error": str(error)}), 500
    else:
        return jsonify({"error": "An unexpected error occurred"}), 500

# ============================
# SQUAD ENDPOINTS
# ============================

@app.route("/api/squads", methods=["POST"])
def create_squad():
    """Create a new squad (no user required)"""
    data = request.get_json()
    
    # Validate input - only name is required
    validation_error = validate_required_fields(data, ["name"])
    if validation_error:
        return jsonify({"error": validation_error}), 400
    
    name = data.get("name")
    commander = data.get("commander", "")  # Optional commander name
    description = data.get("description", "")
    
    try:
        query = "INSERT INTO squads (name, commander, description) VALUES (%s, %s, %s) RETURNING id, name, commander, description"
        squad = execute_query(query, (name, commander, description), fetch_one=True)
        return jsonify(squad), 201
    except Exception as e:
        return handle_error(e)

@app.route("/api/squads", methods=["GET"])
def get_all_squads():
    """Get all squads (accessible to everyone)"""
    try:
        query = "SELECT id, name, commander, description, created_at FROM squads ORDER BY created_at DESC"
        squads = execute_query(query, fetch_all=True)
        return jsonify(squads), 200
    except Exception as e:
        return handle_error(e)

@app.route("/api/squads/<int:squad_id>", methods=["GET"])
def get_squad(squad_id):
    """Get details for a specific squad"""
    try:
        query = "SELECT id, name, commander, description, created_at FROM squads WHERE id = %s"
        squad = execute_query(query, (squad_id,), fetch_one=True)
        
        if squad:
            return jsonify(squad), 200
        else:
            return jsonify({"error": "Squad not found"}), 404
    except Exception as e:
        return handle_error(e)

@app.route("/api/squads/<int:squad_id>", methods=["DELETE"])
def delete_squad(squad_id):
    """Delete a squad (this will also delete all units in the squad due to cascade)"""
    try:
        query = "DELETE FROM squads WHERE id = %s"
        rows_affected = execute_query(query, (squad_id,))
        
        if rows_affected > 0:
            return jsonify({"message": "Squad deleted successfully"}), 200
        else:
            return jsonify({"error": "Squad not found"}), 404
    except Exception as e:
        return handle_error(e)

# ============================
# UNIT ENDPOINTS
# ============================

@app.route("/api/squads/<int:squad_id>/units", methods=["GET"])
def get_squad_units(squad_id):
    """Get all units in a specific squad"""
    try:
        query = "SELECT id, name, race, class, level, armor, weapon FROM units WHERE squad_id = %s ORDER BY name"
        units = execute_query(query, (squad_id,), fetch_all=True)
        return jsonify(units), 200
    except Exception as e:
        return handle_error(e)

@app.route("/api/units", methods=["POST"])
def create_unit():
    """Create a new unit in a squad"""
    data = request.get_json()
    
    # Validate input
    validation_error = validate_required_fields(data, ["squad_id", "name", "class"])
    if validation_error:
        return jsonify({"error": validation_error}), 400
    
    squad_id = data.get("squad_id")
    name = data.get("name")
    race = data.get("race")
    unit_class = data.get("class")
    level = data.get("level", 1)  # Default to level 1
    armor = data.get("armor")
    weapon = data.get("weapon")
    
    try:
        query = """INSERT INTO units (squad_id, name, race, class, level, armor, weapon) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s) 
                   RETURNING id, name, race, class, level, armor, weapon"""
        unit = execute_query(query, (squad_id, name, race, unit_class, level, armor, weapon), fetch_one=True)
        return jsonify(unit), 201
    except Exception as e:
        return handle_error(e)

@app.route("/api/units/<int:unit_id>", methods=["PUT"])
def update_unit(unit_id):
    """Update attributes of an existing unit"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    # Build dynamic update query based on provided fields
    allowed_fields = ["name", "race", "class", "level", "armor", "weapon"]
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = %s")
            values.append(data[field])
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    values.append(unit_id)  # Add unit_id for WHERE clause
    
    try:
        query = f"UPDATE units SET {', '.join(updates)} WHERE id = %s RETURNING id, name, race, class, level, armor, weapon"
        unit = execute_query(query, values, fetch_one=True)
        
        if unit:
            return jsonify(unit), 200
        else:
            return jsonify({"error": "Unit not found"}), 404
    except Exception as e:
        return handle_error(e)

# ============================
# GAME DATA ENDPOINTS
# ============================
# These provide the dropdown options for unit creation/editing

@app.route("/api/races", methods=["GET"])
def get_races():
    """Get all available races for unit creation"""
    try:
        query = "SELECT name, skill, base_HP, base_speed, description FROM races ORDER BY name"
        races = execute_query(query, fetch_all=True)
        return jsonify(races), 200
    except Exception as e:
        return handle_error(e)

@app.route("/api/classes", methods=["GET"])
def get_classes():
    """Get all available classes for unit creation"""
    try:
        query = "SELECT name, skill, description FROM classes ORDER BY name"
        classes = execute_query(query, fetch_all=True)
        return jsonify(classes), 200
    except Exception as e:
        return handle_error(e)

@app.route("/api/armors", methods=["GET"])
def get_armors():
    """Get all available armor types"""
    try:
        query = "SELECT name, defense_bonus, weight, description FROM armors ORDER BY defense_bonus"
        armors = execute_query(query, fetch_all=True)
        return jsonify(armors), 200
    except Exception as e:
        return handle_error(e)

@app.route("/api/weapons", methods=["GET"])
def get_weapons():
    """Get all available weapons"""
    try:
        query = "SELECT name, damage, damage_type, range, description FROM weapons ORDER BY damage"
        weapons = execute_query(query, fetch_all=True)
        return jsonify(weapons), 200
    except Exception as e:
        return handle_error(e)

# ============================
# APPLICATION STARTUP
# ============================

if __name__ == "__main__":
    app.run(debug=config.DEBUG)