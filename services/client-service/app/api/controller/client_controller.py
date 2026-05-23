from flask import Blueprint, request, jsonify
from flasgger import swag_from

from application.services.client_service import ClientService
from domain.entities.client import Client
from api.dto.client_resquest_dto import ClientRequestDto
from api.dto.client_response_dto import ClientResponseDto

client_bp = Blueprint("client", __name__)
service = ClientService()


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
                    "email": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"}
                },
                "required": ["name", "surname", "email", "birthdate"]
            }
        }
    ],
    "responses": {
        201: {"description": "Client created"},
        400: {"description": "Invalid data"}
    }
})
def create_client():
    try:
        dto = ClientRequestDto.from_dict(request.json)

        client = Client(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            birthdate=dto.birthdate
        )

        created = service.create_client(client)

        return jsonify(ClientResponseDto.from_entity(created).to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@client_bp.route('/clients/<string:client_id>', methods=["GET"])
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
        200: {"description": "Client found"},
        404: {"description": "Client not found"}
    }
})
def get_client(client_id):
    if client := service.get_client(client_id):
        return jsonify(ClientResponseDto.from_entity(client).to_dict()), 200
    else:
        return jsonify({"message": "Client not found"}), 404


@client_bp.route('/clients', methods=["GET"])
@swag_from({
    "tags": ["Client"],
    "responses": {
        200: {"description": "List of clients"}
    }
})
def get_all_clients():
    clients = service.get_all_clients()

    return jsonify([
        ClientResponseDto.from_entity(c).to_dict()
        for c in clients
    ]), 200

@client_bp.route('/clients/active', methods=["GET"])
def get_active_clients():
    clients = service.get_active_clients()

    return jsonify([
        ClientResponseDto.from_entity(c).to_dict()
        for c in clients
    ]), 200


@client_bp.route('/clients/inactive', methods=["GET"])
def get_inactive_clients():
    clients = service.get_inactive_clients()

    return jsonify([
        ClientResponseDto.from_entity(c).to_dict()
        for c in clients
    ]), 200


@client_bp.route('/clients/<string:client_id>', methods=["PUT"])
@swag_from({
    "tags": ["Client"],
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
                    "birthdate": {"type": "string", "format": "date"}
                },
                "required": ["name", "surname", "email", "birthdate"]
            }
        }
    ],
    "responses": {
        200: {"description": "Updated successfully"},
        400: {"description": "Invalid data"}
    }
})
def update_client(client_id):
    try:
        dto = ClientRequestDto.from_dict(request.json)

        client = Client(
            name=dto.name,
            surname=dto.surname,
            email=dto.email,
            birthdate=dto.birthdate
        )

        client.id = client_id
        service.update_client(client)

        return jsonify({"message": "updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@client_bp.route('/clients/<string:client_id>', methods=["DELETE"])
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
        400: {"description": "Error deleting client"}
    }
})
def delete_client(client_id):
    try:
        service.delete_client(client_id)
        return jsonify({"message": "deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400