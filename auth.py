from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required

from database import user_collection

auth_bp = Blueprint("auth", __name__)


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email dan password harus di isi!"}), 400

    user = user_collection.find_one({"email": data["email"]})

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Email atau password invalid!"}), 401

    access_token = create_access_token(identity=data["email"])
    return jsonify({"success": "Login berhasil!", "access_token": access_token}), 200


# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Nama, email, dan password harus di isi!"}), 400

    if user_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "Email sudah terdaftar!"}), 400

    hashed_password = generate_password_hash(data["password"])

    user_collection.insert_one(
        {"name": data["name"], "email": data["email"], "password": hashed_password}
    )

    access_token = create_access_token(identity=data["email"])
    return jsonify({"success": "Register berhasil!", "access_token": access_token}), 201


# Read all users
@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = list(user_collection.find())

    for user in users:
        user["_id"] = str(user["_id"])

    return jsonify(users), 200


# TODO: Logout
# TODO: Hapus akun
