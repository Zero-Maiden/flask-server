from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

test_bp = Blueprint("test", __name__)


@test_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Halo dari Flask!"}), 200


@test_bp.route("/test/auth", methods=["GET"])
@jwt_required()
def test_auth():
    current_user = get_jwt_identity()
    return jsonify({"message": "Halo dari Flask!", "current_user": current_user}), 200
