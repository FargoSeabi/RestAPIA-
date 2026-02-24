from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (fake database)
users = [
    {"id": 1, "name": "Moses"},
    {"id": 2, "name": "John"}
]

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to my simple API"})

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# Get single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Add new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
