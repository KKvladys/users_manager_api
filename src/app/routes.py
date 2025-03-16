from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.app.schemas import (
    user_create_schema,
    user_response_schema,
    user_update_schema
)
from src.database.database import db
from src.app.modles import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = user_create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except Exception as e:
        return jsonify({"error": "Invalid input data", "message": str(e)}), 400

    try:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"error": f"Email {existing_user.email} already exists"}), 409

        user = User(name=data["name"], email=data["email"])
        db.session.add(user)
        db.session.commit()

        return jsonify(user_response_schema.dump(user)), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500


@users_bp.route("/users", methods=["GET"])
def get_users():
    """
    Retrieve a list of all users.
    """
    try:
        users = User.query.all()
        return jsonify(user_response_schema.dump(users), many=True)
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500


@users_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    """
    Retrieve a single user by ID.
    """
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user_response_schema.dump(user))
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500


@users_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    """
    Update an existing user data (name, email) by ID.
    """
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = user_update_schema.load(request.get_json())

        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()
        return jsonify(user_response_schema.dump(user))
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500


@users_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    """
    Delete a user by ID.
    """
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500
