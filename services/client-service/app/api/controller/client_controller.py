from flask import Blueprint, request, jsonify
from flasgger import swag_from
from datetime import datetime
from application.services.client_service import ClientService
from domain.entities.client import Client

client_bp = Blueprint("client", __name__)
service = ClientService()


# Criar cliente
@client_bp.route('/clients', methods=["POST"])
@swag_from({
    "tags": ["Client"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                    "email": {"type": "string"},
                    "birthdate": {"type": "string", "format": "date"},
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
        data = request.json
        birthdate = datetime.strptime(data["birthdate"], "%Y-%m-%d")
        client = Client(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            birthdate=birthdate,
        )
        created = service.create_client(client)
        return jsonify(created.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Buscar cliente por ID
@client_bp.route('/clients/<string:client_id>', methods=["GET"])
@swag_from({
    "tags": ["Client"],
    "parameters": [
        {"name": "client_id", "in": "path", "type": "string", "required": True}
    ],
    "responses": {
        200: {"description": "Client found"},
        404: {"description": "Client not found"}
    }
})
def get_client(client_id):
    client = service.get_client(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404
    return jsonify(client.to_dict()), 200


# Buscar todos os clientes
@client_bp.route('/clients', methods=["GET"])
@swag_from({
    "tags": ["Client"],
    "responses": {
        200: {"description": "List of all clients"},
        500: {"description": "Server error"}
    }
})
def get_all_clients():
    clients = service.get_all_clients()
    return jsonify([c.to_dict() for c in clients]), 200


# Buscar clientes ativos
@client_bp.route('/clients/active', methods=["GET"])
@swag_from({
    "tags": ["Client"],
    "responses": {
        200: {"description": "List of active clients"}
    }
})
def get_active_clients():
    clients = service.get_active_clients()
    return jsonify([c.to_dict() for c in clients]), 200


# Buscar clientes inativos
@client_bp.route('/clients/inactive', methods=["GET"])
@swag_from({
    "tags": ["Client"],
    "responses": {
        200: {"description": "List of inactive clients"}
    }
})
def get_inactive_clients():
    clients = service.get_inactive_clients()
    return jsonify([c.to_dict() for c in clients]), 200


# Atualizar cliente
@client_bp.route('/clients/<string:client_id>', methods=["PUT"])
@swag_from({
    "tags": ["Client"],
    "parameters": [
        {"name": "client_id", "in": "path", "type": "string", "required": True},
        {
            "name": "body",
            "in": "body",
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
        200: {"description": "Client updated successfully"},
        404: {"description": "Client not found"},
        400: {"description": "Invalid data"}
    }
})
def update_client(client_id):
    try:
        data = request.json
        birthdate = datetime.strptime(data["birthdate"], "%Y-%m-%d")
        client = Client(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            birthdate=birthdate
        )
        client.id = client_id
        service.update_client(client)
        return jsonify({"message": "Client updated successfully", "id": client_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Deletar cliente (lógico)
@client_bp.route('/clients/<string:client_id>', methods=["DELETE"])
@swag_from({
    "tags": ["Client"],
    "parameters": [
        {"name": "client_id", "in": "path", "type": "string", "required": True}
    ],
    "responses": {
        200: {"description": "Client disabled successfully"},
        404: {"description": "Client not found"},
        400: {"description": "Error disabling client"}
    }
})
def delete_client(client_id):
    try:
        service.delete_client(client_id)
        return jsonify({"message": "Client disabled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400