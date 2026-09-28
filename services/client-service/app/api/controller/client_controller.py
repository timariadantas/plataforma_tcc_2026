import time

from flask import Blueprint, request, jsonify ,g 
from flasgger import swag_from

from infrastructure.container import client_service
from domain.entities.client import Client

from api.dto.client_request_dto import CreateClientRequestDto
from api.dto.client_response_dto import ClientResponseDto
from api.dto.update_client_request_dto import UpdateClientRequestDto
from api.dto.change_password_request_dto import ChangePasswordRequestDto
from api.dto.api_response import ApiResponse


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
                    "name": {
                        "type": "string",
                        "example": "Maria"
                    },
                    "surname": {
                        "type": "string",
                        "example": "Dantas"
                    },
                    "email": {
                        "type": "string",
                        "example": "maria@email.com"
                    },
                    "password": {
                        "type": "string",
                        "example": "Senha@123"
                    },
                    "birthdate": {
                        "type": "string",
                        "format": "date",
                        "example": "1995-05-20"
                    }
                },
                "required": [
                    "name",
                    "surname",
                    "email",
                    "password",
                    "birthdate"
                ]
            }
        }
    ],

    "responses": {

        201: {
            "description": "Client created successfully",
            "schema": {
                "$ref": "#/definitions/ClientResponse"
            }
        },

        400: {
            "description": "Invalid client data",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        409: {
            "description": "Email already exists",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def create_client():

    dto = CreateClientRequestDto.from_dict(request.json)

    client = Client(
        name=dto.name,
        surname=dto.surname,
        email=dto.email,
        password_hash=dto.password,
        birthdate=dto.birthdate
    )

    created = client_service.create_client(client)
    
    elapsed = int( 
                  (time.perf_counter() - g.start_time) * 1000 )

    api_response = ApiResponse( 
            message="Client created successfully",
            elapsed=elapsed, 
            data=ClientResponseDto.from_entity(created).to_dict())
            
    return jsonify(api_response.to_dict()), 201




@client_bp.route('/clients/<string:client_id>', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Get a client",
    "description": "Returns a client by its ID.",
    "security": [{"Bearer": []}],

    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Client ID"
        }
    ],

    "responses": {
        200: {
            "description": "Client found",
            "schema": {
                "$ref": "#/definitions/ClientResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        404: {
            "description": "Client not found",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_client(client_id):

    client = client_service.get_client(client_id)

    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    
    api_response = ApiResponse( 
                               
        message="Client found", 
        elapsed=elapsed, 
        data=ClientResponseDto.from_entity(client).to_dict() 
        
        ) 
    
    return jsonify(api_response.to_dict()), 200



@client_bp.route('/internal/clients/<string:client_id>', methods=["GET"])
def get_client_internal(client_id):

    client = client_service.get_client(client_id)

    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    api_response = ApiResponse( 
        message="Client found", 
        elapsed=elapsed, 
        data=ClientResponseDto.from_entity(client).to_dict() ) 
    
    return jsonify(api_response.to_dict()), 200




@client_bp.route('/clients', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Get all clients",
    "description": "Returns all clients.",
    "security": [{"Bearer": []}],

    "responses": {
        200: {
            "description": "List of clients",
            "schema": {
                "$ref": "#/definitions/ClientListResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_all_clients():

    clients = client_service.get_all_clients()

    data = [ 
            ClientResponseDto.from_entity(client).to_dict()
            for client in clients ] 
    
    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    api_response = ApiResponse( 
        message="Clients retrieved successfully", 
        elapsed=elapsed, 
        data=data ) 
    
    return jsonify(api_response.to_dict()), 200



@client_bp.route('/clients/active', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Get active clients",
    "description": "Returns all active clients.",
    "security": [{"Bearer": []}],

    "responses": {
        200: {
            "description": "List of active clients",
            "schema": {
                "$ref": "#/definitions/ClientListResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_active_clients():

    clients = client_service.get_active_clients()

    data = [ 
            ClientResponseDto.from_entity(client).to_dict() 
            for client in clients ] 
    
    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    
    api_response = ApiResponse( 
        message="Active clients retrieved successfully", 
        elapsed=elapsed, 
        data=data ) 
    
    return jsonify(api_response.to_dict()), 200



@client_bp.route('/clients/inactive', methods=["GET"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Get inactive clients",
    "description": "Returns all inactive clients.",
    "security": [{"Bearer": []}],

    "responses": {
        200: {
            "description": "List of inactive clients",
            "schema": {
                "$ref": "#/definitions/ClientListResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_inactive_clients():

    clients = client_service.get_inactive_clients()

    data = [ 
            ClientResponseDto.from_entity(client).to_dict() 
            for client in clients ] 
    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    api_response = ApiResponse( 
        message="Inactive clients retrieved successfully", 
        elapsed=elapsed, 
        data=data ) 
    return jsonify(api_response.to_dict()), 200


@client_bp.route('/clients/<string:client_id>', methods=["PUT"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Update a client",
    "description": "Updates the client's basic information.",
    "security": [{"Bearer": []}],
    "consumes": ["application/json"],

    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Client ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Maria"
                    },
                    "surname": {
                        "type": "string",
                        "example": "Dantas"
                    },
                    "email": {
                        "type": "string",
                        "example": "maria.nova@email.com"
                    }
                },
                "required": [
                    "name",
                    "surname",
                    "email"
                ]
            }
        }
    ],

    "responses": {
        200: {
            "description": "Client updated successfully",
            "schema": {
                "$ref": "#/definitions/ClientResponse"
            }
        },
        400: {
            "description": "Invalid client data",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        404: {
            "description": "Client not found",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        409: {
            "description": "Email already exists",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def update_client(client_id):

    dto = UpdateClientRequestDto.from_dict(request.json)

    client = client_service.update_client(
        client_id=client_id,
        name=dto.name,
        surname=dto.surname,
        email=dto.email
    )

    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    api_response = ApiResponse( 
        message="Client updated successfully", 
        elapsed=elapsed, 
        data=ClientResponseDto.from_entity(client).to_dict() 
    ) 
    
    return jsonify(api_response.to_dict()), 200



@client_bp.route(
    "/clients/<string:client_id>/password",
    methods=["PATCH"]
)
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Change client password",
    "description": "Updates the client's password.",
    "security": [{"Bearer": []}],
    "consumes": ["application/json"],

    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Client ID"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "new_password": {
                        "type": "string",
                        "example": "NovaSenha@123"
                    }
                },
                "required": [
                    "new_password"
                ]
            }
        }
    ],

    "responses": {
        200: {
            "description": "Password updated successfully",
            "schema": {
                "$ref": "#/definitions/MessageResponse"
            }
        },
        400: {
            "description": "Invalid password data",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        404: {
            "description": "Client not found",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def change_password(client_id):

    dto = ChangePasswordRequestDto.from_dict(request.json)

    client_service.change_password(
        client_id=client_id,
        new_password=dto.new_password
    )
    
    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    
    api_response = ApiResponse( 
        message="Password updated successfully", 
        elapsed=elapsed 
    ) 
    return jsonify(api_response.to_dict()), 200

   


@client_bp.route('/clients/<string:client_id>', methods=["DELETE"])
@token_required
@swag_from({
    "tags": ["Client"],
    "summary": "Deactivate a client",
    "description": "Soft deletes a client by setting it as inactive.",
    "security": [{"Bearer": []}],

    "parameters": [
        {
            "name": "client_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Client ID"
        }
    ],

    "responses": {
        200: {
            "description": "Client deactivated successfully",
            "schema": {
                "$ref": "#/definitions/MessageResponse"
            }
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        404: {
            "description": "Client not found",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        503: {
            "description": "Client service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def delete_client(client_id):

    client_service.delete_client(client_id)

    elapsed = int( (time.perf_counter() - g.start_time) * 1000 ) 
    api_response = ApiResponse( 
        message="Client deactivated successfully", 
        elapsed=elapsed 
    ) 
    return jsonify(api_response.to_dict()), 200