"""
WARGAME BACKEND API
A simple Flask API for managing squads and units in a medieval wargame.
No user system - anyone can create and view squads.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import glob
import re

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
# API ENDPOINTS
# ============================

# Create new squad
@app.route("/api/squads", methods=["POST"])
def create_squad():
    data = request.get_json()
    
    # Validate input - only name is required
    validation_error = validate_required_fields(data, ["name"])
    if validation_error:
        return jsonify({"error": validation_error}), 400
    
    name = data.get("name")
    commander = data.get("commander", "") 
    description = data.get("description", "")
    
    try:
        query = "INSERT INTO squads (name, commander, description) VALUES (%s, %s, %s) RETURNING id, name, commander, description"
        squad = execute_query(query, (name, commander, description), fetch_one=True)
        return jsonify(squad), 201
    except Exception as e:
        return handle_error(e)

# Get all squads
@app.route("/api/squads", methods=["GET"])
def get_all_squads():
    try:
        query = "SELECT id, name, commander, description, created_at FROM squads ORDER BY created_at DESC"
        squads = execute_query(query, fetch_all=True)
        return jsonify(squads), 200
    except Exception as e:
        return handle_error(e)

# Get a specific squad
@app.route("/api/squads/<int:squad_id>", methods=["GET"])
def get_squad(squad_id):
    try:
        query = "SELECT id, name, commander, description, created_at FROM squads WHERE id = %s"
        squad = execute_query(query, (squad_id,), fetch_one=True)
        
        if squad:
            return jsonify(squad), 200
        else:
            return jsonify({"error": "Squad not found"}), 404
    except Exception as e:
        return handle_error(e)

# Delete a squad by id (cascade deletes all units in that squad)
@app.route("/api/squads/<int:squad_id>", methods=["DELETE"])
def delete_squad(squad_id):
    try:
        query = "DELETE FROM squads WHERE id = %s"
        rows_affected = execute_query(query, (squad_id,))
        
        if rows_affected > 0:
            return jsonify({"message": "Squad deleted successfully"}), 200
        else:
            return jsonify({"error": "Squad not found"}), 404
    except Exception as e:
        return handle_error(e)


# Get all units in a specific squad
@app.route("/api/squads/<int:squad_id>/units", methods=["GET"])
def get_squad_units(squad_id):
    try:
        query = "SELECT id, name, race, class, level, armor, weapon FROM units WHERE squad_id = %s ORDER BY name"
        units = execute_query(query, (squad_id,), fetch_all=True)
        return jsonify(units), 200
    except Exception as e:
        return handle_error(e)

# Create a new unit in a squad
@app.route("/api/units", methods=["POST"])
def create_unit():
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

# # Update an existing unit
# @app.route("/api/units/<int:unit_id>", methods=["PUT"])
# def update_unit(unit_id):
#     """Update attributes of an existing unit"""
#     data = request.get_json()
    
#     if not data:
#         return jsonify({"error": "Request body is required"}), 400
    
#     # Build dynamic update query based on provided fields
#     allowed_fields = ["name", "race", "class", "level", "armor", "weapon"]
#     updates = []
#     values = []
    
#     for field in allowed_fields:
#         if field in data:
#             updates.append(f"{field} = %s")
#             values.append(data[field])
    
#     if not updates:
#         return jsonify({"error": "No valid fields to update"}), 400
    
#     values.append(unit_id)  # Add unit_id for WHERE clause
    
#     try:
#         query = f"UPDATE units SET {', '.join(updates)} WHERE id = %s RETURNING id, name, race, class, level, armor, weapon"
#         unit = execute_query(query, values, fetch_one=True)
        
#         if unit:
#             return jsonify(unit), 200
#         else:
#             return jsonify({"error": "Unit not found"}), 404
#     except Exception as e:
#         return handle_error(e)

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
# BATTLE REPORT ENDPOINT
# ============================

@app.route("/api/battle-report", methods=["GET"])
def get_latest_battle_report():
    """Get the content of the most recent battle report file"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get the project root, then into reports
        reports_dir = os.path.join(os.path.dirname(script_dir), "reports")
        
        # Find all battle report files
        pattern = os.path.join(reports_dir, "battle_report_*.txt")
        report_files = glob.glob(pattern)
        
        if not report_files:
            return jsonify({
                "content": "No battle reports found.",
                "filename": None,
                "timestamp": None
            }), 200
        
        # Sort files by modification time (most recent first)
        report_files.sort(key=os.path.getmtime, reverse=True)
        latest_file = report_files[0]
        
        # Extract timestamp from filename
        filename = os.path.basename(latest_file)
        timestamp_match = re.search(r'battle_report_(\d{8}_\d{6})\.txt', filename)
        timestamp = timestamp_match.group(1) if timestamp_match else None
        
        # Read the file content
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "content": content,
            "filename": filename,
            "timestamp": timestamp
        }), 200
        
    except Exception as e:
        return handle_error(e)

# ============================
# APPLICATION STARTUP
# ============================

if __name__ == "__main__":
    app.run(debug=config.DEBUG)