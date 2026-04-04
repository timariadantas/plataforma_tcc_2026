from flask import Blueprint, request, jsonify
from flasgger import swag_from

from application.services.client_service import ClientService
from domain.entities.client import Client

client_bp = Blueprint("client", __name__)
service = ClientService()

@client_bp.route("/clients", methods=["POST"])
@swag_from({
    "tags": [Client],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type" : "object",
                "properties":{
                    "name": {"type": "string"},
                    "surname": {"type" : "string"},
                    "email" : {"type": "string"},
                    "birthdate" : {"type" : "string"},
                }
            }
        }
    ],
    "responses" : {
        201: {"descripton": "Client created"},
        400: {"description" : "Invalid data"}
    }
    
})
def create_client():
    try:
        data = request.json
        
        client = Client(
            name = data["name"],
            surname = data["surname"],
            email = data["email"],
            birthdate = data["birthdate"],
        )
        created = service.create_client(client)
        return jsonify(created.to_dict()),201
        
    except Exception as e:
        return jsonify({"error":str(e)}),400
    
@client_bp.route("/clients/<client_id", methods=["GET"])
def get_client(client_id):
    try:
        client = service.get_client(client_id)
        
        if not client:
            return jsonify({"messege": "Client not found"}), 404
        return jsonify(client.to_dict),200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client_bp.route("/clients", methods =["GET"])
def get_all_clients():
    try:
        clients = service.get_all_clients()
        return jsonify ([c.to_dict() for c in clients]), 200
    
    except Exception as e:
        return jsonify ({"error": str(e)}), 500
    
@client_bp.route("/clients/active", methods=["GET"])
def get_active_clients():
    try:
        clients = service.get_active_clients()
        return jsonify([c.to_dict() for c in clients]), 200  
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client_bp.route("/clients/inactive", methods=["GET"])
def get_inactive_clients():
    try:
        clients = service.get_inactive_clients()
        return jsonify([c.to_dict() for c in clients]),200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@client_bp.route("/clients/<client_id", methods=["PUT"])
def update_client(client_id):
    try:
        data = request.json

        client = Client(
            name = data["name"],
            surname= data["surname"],
            email=data["email"],
            birthdate= data["birthdate"]
        )
        existing = service.get_client(client_id)
        if not existing:
            return jsonify({"message": "Client not found"}), 404,
        
        client.id=client_id
        service.update_client(client)
        
        return jsonify({
            "messege" : "Client update sucessfully",
            "id": client_id
        }),200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@client_bp.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    try:
        existing = service.get_client(client_id)
        if not existing:
            return jsonify({"message": "Client not found"}), 404

        service.delete_client(client_id)
        return jsonify({"message": "Client disable sucessfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
