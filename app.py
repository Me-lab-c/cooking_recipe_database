from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='hrishi@2006',  # your real MySQL password
        database='foodbuggy'
    )

@app.route('/')
def home():
    return "Flask server is running!"

# Fetch all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, description, image_url FROM recipes")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

# Add a new recipe
@app.route('/submit', methods=['POST'])
def submit_recipe():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    quantity = data.get('quantity')

    if not title or not description or not quantity:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (title, description, quantity) VALUES (%s, %s, %s)",
        (title, description, quantity)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Recipe submitted successfully!"}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(port=3001, debug=True)
