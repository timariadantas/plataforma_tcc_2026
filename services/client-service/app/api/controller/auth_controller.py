from flask import Blueprint, request, jsonify
from infrastructure.container import auth_service
from infrastructure.errors.service_errors import AuthenticationError , DatabaseUnavailableError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])

def login():
    try:
        data = request.json
        token = auth_service.login(
            email= data.get("email"),
            password = data.get("password")
        )
        
        return jsonify({
            "token" : token
        }),200
        
    except AuthenticationError as e:
        return jsonify({
            "error" : str(e)
        }), 401
        
    except DatabaseUnavailableError as e:
        return jsonify({
            "error": str(e)
        }), 500
        