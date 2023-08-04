from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT,
                 email TEXT,
                 password TEXT)''')
    conn.commit()
    conn.close()

@app.route('/save_user_data', methods=['POST', 'OPTIONS'])  # Include 'OPTIONS' method
def save_user_data():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'message': 'Preflight request handled successfully.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    # Handle actual POST request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    print(data)

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User information saved successfully!'}), 200

# @app.route('/check_credentials', methods=['POST'])
# def check_credentials():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE username = ?", (username,))
#     user = c.fetchone()
#     conn.close()

#     if user and user[3] == password:
#         return jsonify({'message': 'Credentials are valid.'}), 200
#     else:
#         return jsonify({'message': 'Invalid credentials.'}), 401

@app.route('/check_credentials', methods=['POST', 'OPTIONS'])  # Add OPTIONS method
def check_credentials():
    if request.method == 'OPTIONS':
        # Handle pre-flight request
        response = jsonify({'message': 'Preflight request handled.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    # Handle actual POST request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(username,password)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user and user[3] == password:
        return jsonify({'message': 'Credentials are valid.'}), 200
    else:
        return jsonify({'message': 'Invalid credentials.'}), 401

if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)