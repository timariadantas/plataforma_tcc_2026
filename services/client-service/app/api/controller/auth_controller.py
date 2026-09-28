import time
from flask import Blueprint, request, jsonify, g
from infrastructure.container import auth_service
from api.dto.api_response import ApiResponse
from flasgger import swag_from
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
@swag_from({
    "tags": ["Authentication"],
    "summary": "Authenticate client",
    "description": "Authenticates a client using email and password and returns a JWT token.",
    "consumes": ["application/json"],

    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "format": "email",
                        "example": "maria@email.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "Senha@123"
                    }
                },
                "required": [
                    "email",
                    "password"
                ]
            }
        }
    ],

    "responses": {
        200: {
            "description": "Login successful",
            "schema": {
                "$ref": "#/definitions/LoginResponse"
            }
        },
        401: {
            "description": "Invalid credentials",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def login():
    
    data = request.json
    token = auth_service.login(
        email= data.get("email"),
        password = data.get("password")
    )
    elapsed = int( 
        (time.perf_counter() - g.start_time) * 1000 )
        
    api_response = ApiResponse( 
        message="Login successful", 
        elapsed=elapsed, 
        data={ "token": token } 
    )
    return jsonify(api_response.to_dict()), 200