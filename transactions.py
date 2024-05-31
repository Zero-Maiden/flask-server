from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId

from database import transaction_collection

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/", methods=["POST"])
@jwt_required()
def create_transaction():
    transaction = request.get_json()

    if not transaction:
        return jsonify({"error": "Semua harus di isi!"}), 400

    transaction_collection.insert_one(transaction)

    return jsonify({"success": "Transaksi berhasil di input!"}), 201


@transactions_bp.route("/", methods=["GET"])
@jwt_required()
def test_transaction():
    transactions = list(transaction_collection.find())

    for transaction in transactions:
        transaction["_id"] = str(transaction["_id"])

    return jsonify(transactions), 200


@transactions_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(id):
    result = transaction_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Transaksi tidak ditemukan!"}), 404

    return jsonify({"success": "Transaksi berhasil dihapus!"}), 200
