from flask import Blueprint, request, jsonify
from flasgger import swag_from
from infrastructure.container import client_service
from domain.entities.client import Client
from api.dto.client_resquest_dto import ClientRequestDto
from api.dto.client_response_dto import ClientResponseDto
from api.dto.change_password_request_dto import ChangePasswordRequestDto
from infrastructure.errors.service_errors import (DatabaseUnavailableError, ClientNotFoundError)
from infrastructure.security.auth_middleware import token_required


client_bp = Blueprint("client", __name__)

@client_bp.route('/clients', methods=["POST"])
@swag_from({
    "tags": ["Client"],
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                    "password": {"type": "string"},
                    "email": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"}
                },
                "required": ["name", "surname", "email", "password", "birthdate"]
            }
        }
    ],
    "responses": {
        201: {"description": "Client created"},
        400: {"description": "Invalid data"},
        503: {"description": "Service unavailable"}
    }
})
def create_client():
    try:
        dto = ClientRequestDto.from_dict(request.json)

        client = Client(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            password_hash=dto.password,
            birthdate=dto.birthdate
        )

        created = client_service.create_client(client)
        return jsonify(ClientResponseDto.from_entity(created).to_dict()), 201
        

    except DatabaseUnavailableError:
        return jsonify({
                        "message": "Client service temporarily unavailable",
                        "fallback" : True
                        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        


@client_bp.route('/clients/<string:client_id>', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Client found"},
        401: {"description": "Unauthorized"},
        404: {"description": "Client not found"},
        503: {"description": "Service unavailable"}
    }
})
def get_client(client_id):
    try:
        client = client_service.get_client(client_id)
        return jsonify(ClientResponseDto.from_entity(client).to_dict()), 200
    
    except ClientNotFoundError:
        return jsonify({"message": "Client not found"}), 404
    
    except DatabaseUnavailableError:
        return jsonify({
            "messege": "Client service temporarily unavailable",
            "fallback" : True
        }), 503

@client_bp.route('/internal/clients/<string:client_id>', methods=["GET"])
def get_client_internal(client_id):
    try:
        client = client_service.get_client(client_id)
        return jsonify(ClientResponseDto.from_entity(client).to_dict()), 200

    except ClientNotFoundError:
        return jsonify({"message": "Client not found"}), 404

    except DatabaseUnavailableError:
        return jsonify({
            "message": "Client service temporarily unavailable",
            "fallback": True
        }), 503

@client_bp.route('/clients', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "security": [{"Bearer": []}],
    "responses": {
        200: {"description": "List of clients"},
        401: {"description": "Unauthorized"},
        503: {"description": "Service unavailable"}
    }
})
def get_all_clients():
    try:
        clients = client_service.get_all_clients()

        return jsonify([
            ClientResponseDto.from_entity(c).to_dict()
            for c in clients
        ]), 200
        
    except DatabaseUnavailableError:
        return jsonify({
            "messege" : "Client service temporarily unavailable",
            "fallback" : True
        }), 503
        
    
    

@client_bp.route('/clients/active', methods=["GET"])
@token_required
def get_active_clients():
    try :
        clients = client_service.get_active_clients()

        return jsonify([
            ClientResponseDto.from_entity(c).to_dict()
            for c in clients
    ]), 200
    
    except DatabaseUnavailableError:
        return jsonify({
            "message": "Service temporarily unavailable",
            "fallback": True
        }), 503
            
    


@client_bp.route('/clients/inactive', methods=["GET"])
@token_required
def get_inactive_clients():
    try:
        clients = client_service.get_inactive_clients()

        return jsonify([
            ClientResponseDto.from_entity(c).to_dict()
            for c in clients
        ]), 200
        
    except DatabaseUnavailableError:
        return jsonify({
            "message": "Service temporarily unavailable",
            "fallback": True
        }), 503


@client_bp.route('/clients/<string:client_id>', methods=["PUT"])
@token_required
@swag_from({
    "tags": ["Client"],
    "security": [{"Bearer": []}],
    "consumes": ["application/json"],
    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"}
                },
                "required": ["name", "surname", "email", "birthdate"]
            }
        }
    ],
    "responses": {
        200: {"description": "Updated successfully"},
        400: {"description": "Invalid data"},
        503: {"description": "Service unavailable"}
    }
})
def update_client(client_id):
    try:
        dto = ClientRequestDto.from_dict(request.json)

        client = Client(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            password_hash=dto.password,
            birthdate=dto.birthdate
        )

        client.id = client_id
        client_service.update_client(client)

        return jsonify({"message": "updated"}), 200
    
    except DatabaseUnavailableError:
        return jsonify({
            "message": "Service temporarily unavailable",
            "fallback": True
        }), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@client_bp.route("/clients/<string:client_id>/password", methods=["PATCH"])
@token_required
def change_password(client_id):
    try:
        dto = ChangePasswordRequestDto.from_dict(request.json)

        client_service.change_password(
            client_id,
            dto.new_password
        )

        return jsonify({
            "message": "Password updated successfully"
        }), 200

    except DatabaseUnavailableError:
        return jsonify({
            "message": "Client service temporarily unavailable",
            "fallback": True
        }), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
@client_bp.route('/clients/<string:client_id>', methods=["DELETE"])
@token_required
@swag_from({
    "tags": ["Client"],
    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Deleted successfully"},
        400: {"description": "Error deleting client"},
        503: {"description": "Service unavailable"}
    }
})
def delete_client(client_id):
    try:
        client_service.delete_client(client_id)
        return jsonify({"message": "deleted"}), 200

    except DatabaseUnavailableError:
        return jsonify({
            "message": "Service temporarily unavailable",
            "fallback": True
        }), 503
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400