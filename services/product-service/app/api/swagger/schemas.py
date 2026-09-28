PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
            "example": "01K2ABC123XYZ"
        },
        "name": {
            "type": "string",
            "example": "Notebook Dell"
        },
        "description": {
            "type": "string",
            "nullable": True,
            "example": "Notebook para desenvolvimento"
        },
        "price": {
            "type": "number",
            "format": "float",
            "example": 3500.00
        },
        "quantity": {
            "type": "integer",
            "example": 10
        }
    },
    "required": [
        "id",
        "name",
        "price",
        "quantity"
    ]
}


PRODUCT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Product found"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 12
        },
        "data": {
            "$ref": "#/definitions/Product"
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed",
        "data"
    ]
}


PRODUCT_LIST_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Products retrieved successfully"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 15
        },
        "data": {
            "type": "object",
            "properties": {
                "products": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Product"
                    }
                },
                "page": {
                    "type": "integer",
                    "example": 1
                },
                "limit": {
                    "type": "integer",
                    "example": 10
                }
            },
            "required": [
                "products",
                "page",
                "limit"
            ]
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed",
        "data"
    ]
}


MESSAGE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Product deleted successfully"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 10
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed"
    ]
}


STOCK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Stock found"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 8
        },
        "data": {
            "type": "object",
            "properties": {
                "quantity": {
                    "type": "integer",
                    "example": 10
                }
            },
            "required": [
                "quantity"
            ]
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed",
        "data"
    ]
}


PRICE_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Price found"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 8
        },
        "data": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "number",
                    "format": "float",
                    "example": 3500.00
                }
            },
            "required": [
                "price"
            ]
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed",
        "data"
    ]
}


ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string",
            "example": "Product not found"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "example": "2026-09-07T18:00:00Z"
        },
        "elapsed": {
            "type": "integer",
            "example": 8
        },
        "error": {
            "type": "string",
            "example": "Product does not exist"
        }
    },
    "required": [
        "message",
        "timestamp",
        "elapsed",
        "error"
    ]
}