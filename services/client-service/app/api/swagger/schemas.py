CLIENT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "example": "01K2ABC123XYZ"
        },
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
        "birthdate": {
            "type": "string",
            "format": "date",
            "example": "1995-05-20"
        },
        "active": {
            "type": "boolean",
            "example": True
        }
    }
}


CLIENT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Client found"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "elapsed": {
            "type": "integer",
            "example": 12
        },
        "data": {
            "$ref": "#/definitions/Client"
        }
    }
}


CLIENT_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Clients retrieved successfully"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "elapsed": {
            "type": "integer",
            "example": 8
        },
        "data": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/Client"
            }
        }
    }
}


MESSAGE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Password updated successfully"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "elapsed": {
            "type": "integer",
            "example": 5
        }
    }
}


LOGIN_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Login successful"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "elapsed": {
            "type": "integer",
            "example": 10
        },
        "data": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "example": "eyJhbGciOiJIUzI1NiIs..."
                }
            }
        }
    }
}


ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Request failed"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "elapsed": {
            "type": "integer",
            "example": 3
        },
        "error": {
            "type": "string",
            "example": "Client not found"
        }
    }
}