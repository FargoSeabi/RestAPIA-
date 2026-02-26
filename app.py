from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
        }

# Create database
with app.app_context():
    db.create_all()

# -----------------------------
# Routes
# -----------------------------

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Advanced Flask API Running"}), 200


# Create user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    # Check if email already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# Get single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


# Update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]

    db.session.commit()

    return jsonify(user.to_dict()), 200


# Delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
