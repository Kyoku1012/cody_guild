# Guild API Server - Simple Flask version
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Simple guild data
guilds = [
    {"id": 1, "name": "Warriors Guild", "user_id": 1},
    {"id": 2, "name": "Mages Guild", "user_id": 2},
    {"id": 3, "name": "Thieves Guild", "user_id": 1}
]

def get_user_info_from_login_server(user_id):
    """
    This is the key function for integration testing.
    It calls the login server to get user information.
    """
    try:
        response = requests.get(f"http://localhost:5001/user/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

@app.route('/guilds/<int:user_id>')
def get_user_guilds(user_id):
    # Integration point: get user info from login server
    user_info = get_user_info_from_login_server(user_id)
    
    if not user_info:
        return jsonify({"error": "User not found"}), 404
    
    # Get guilds for this user
    user_guilds = [guild for guild in guilds if guild["user_id"] == user_id]
    
    return jsonify({
        "user": user_info,
        "guilds": user_guilds
    })

@app.route('/guilds')
def get_all_guilds():
    return jsonify(guilds)

if __name__ == '__main__':
    print("Guild API Server starting on port 5000")
    print("Endpoints:")
    print("  GET /guilds - Get all guilds")
    print("  GET /guilds/<user_id> - Get guilds for user (calls login server)")
    app.run(debug=True, port=5000)
