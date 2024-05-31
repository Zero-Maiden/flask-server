from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId

from database import product_collection

products_bp = Blueprint("products", __name__)


@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    product = request.get_json()

    if (
        not product
        or "name" not in product
        or "category" not in product
        or "description" not in product
        or "price" not in product
    ):
        return jsonify({"error": "Semua harus di isi!"}), 400

    product_collection.insert_one(
        {
            "name": product["name"],
            "category": product["category"],
            "description": product["description"],
            "price": product["price"],
        }
    )

    return jsonify({"success": "Produk berhasil di input!"}), 201


@products_bp.route("/", methods=["GET"])
@jwt_required()
def get_products():
    products = list(product_collection.find())

    for product in products:
        product["_id"] = str(product["_id"])

    return jsonify(products), 200


@products_bp.route("/<id>", methods=["GET"])
@jwt_required()
def get_product(id):
    product = product_collection.find_one({"_id": ObjectId(id)})

    if not product:
        return jsonify({"message": "Produk tidak ditemukan!"}), 400

    product["_id"] = str(product["_id"])

    return jsonify(product), 200


@products_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Inputan kosong!"}), 400

    result = product_collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    if result.matched_count == 0:
        return jsonify({"error": "Produk tidak ditemukan!"}), 404

    return jsonify({"success": "Produk berhasil di update!"}), 200


@products_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    result = product_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Produk tidak ditemukan!"}), 404

    return jsonify({"success": "Produk berhasil dihapus!"}), 200
