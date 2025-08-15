from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Enable CORS for the GitHub Pages origin
CORS(app, resources={r"/api/*": {"origins": "https://charliesaid.github.io"}}) 

# Load environment variables
load_dotenv()

# Connect to Neon database
conn = psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)
cursor = conn.cursor()

# Endpoint to create a user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()  # Get JSON data from the request
    username = data.get("username")
    email = data.get("email")
    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400  # Bad request error
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id, username, email",
            (username, email)
        )
        user = cursor.fetchone()  # Get the inserted row
        conn.commit()  # Save changes
        return jsonify(user), 201  # Success response
    except Exception as e:
        conn.rollback()  # Undo changes on error
        return jsonify({"error": str(e)}), 500  # Server error

# Endpoint to create a squad
@app.route("/api/squads", methods=["POST"])
def create_squad():
    data = request.get_json()
    user_id = data.get("user_id")
    squad_name = data.get("name")
    description = data.get("description", "")  # Optional field
    if not user_id or not squad_name:
        return jsonify({"error": "User ID and squad name are required"}), 400
    try:
        cursor.execute(
            "INSERT INTO squads (user_id, name, description) VALUES (%s, %s, %s) RETURNING id, name, description",
            (user_id, squad_name, description)
        )
        squad = cursor.fetchone()
        conn.commit()
        return jsonify(squad), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

# Endpoint to list squads for a user (GET method)
@app.route("/api/users/<int:user_id>/squads", methods=["GET"])
def get_user_squads(user_id):
    try:
        cursor.execute("SELECT id, name, description FROM squads WHERE user_id = %s", (user_id,))
        squads = cursor.fetchall()  # Get all matching rows
        return jsonify(squads), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Run in debug mode locally