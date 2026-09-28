import time
from flask import Blueprint, request, jsonify , g
from flasgger import swag_from


from api.dto.response.product_response_dto import ProductResponseDto
from api.dto.request.decrease_stock_dto import DecreaseStockDto
from api.dto.request.product_request_dto import ProductRequestDto
from api.dto.response.api_response import ApiResponse

from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.errors.service_errors import InvalidProductDataError
from application.service.product_service import ProductService

from infrastructure.logging.logger import get_logger
from infrastructure.security.auth_middleware import token_required



product_blueprint = Blueprint("product", __name__)

logger = get_logger(__name__)

def get_service():
    repository = ProductRepository()
    return ProductService(repository)


@product_blueprint.route("/products", methods=["POST"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

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
                        "example": "Notebook Dell"
                    },
                    "description": {
                        "type": "string",
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
                    "name",
                    "price",
                    "quantity"
                ]
            }
        }
    ],

    "responses": {

        201: {
            "description": "Product created successfully",
            "schema": {
                "$ref": "#/definitions/ProductResponse"
            }  
        },

        400: {
            "description": "Invalid product data",
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

        500: {
            "description": "Internal server error",
            "schema": {
        "$ref": "#/definitions/ErrorResponse"
    }
        },

        503: {
            "description": "Service unavailable",
            "schema": {
        "$ref": "#/definitions/ErrorResponse"
    }
        }
    }
})
def create_product():

    logger.info("POST /products")

    dto = ProductRequestDto(**request.json)

    user = request.user
    user_id = user["client_id"]

    service = get_service()

    product = service.create_product(dto, user_id)

    response = ProductResponseDto(**product)

    elapsed = int( 
        (time.perf_counter() - g.start_time) * 1000 
    ) 
    api_response = ApiResponse( 
        message="Product created successfully", 
        elapsed=elapsed, data=response.model_dump()
    )
    return jsonify(api_response.to_dict()), 201
     


@product_blueprint.route("/products", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 1,
            "example": 1,
            "description": "Page number. Must be greater than zero."
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 10,
            "example": 10,
            "description": "Number of products per page. Must be greater than zero."
        }
    ],

    "responses": {

        200: {
            "description": "Products retrieved successfully",
            "schema": {
                "$ref": "#/definitions/ProductListResponse"
            }
        },
        400: {
            "description": "Invalid pagination parameters",
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

        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        503: {
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_all_products():

    logger.info("GET /products")
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        
    except (TypeError, ValueError) as e :
        raise InvalidProductDataError("Page and limit must be integers") from e

    if page < 1:

        raise InvalidProductDataError("Page must be greater than zero")

    if limit < 1:

        raise InvalidProductDataError("Limit must be greater than zero")

    service = get_service()

    products = service.get_all_products(page, limit)

    data = [
        ProductResponseDto(**p).model_dump()
        for p in products
        ]

    elapsed = int(
        (time.perf_counter() - g.start_time) * 1000 )
    
    api_response = ApiResponse( 
        message="Products retrieved successfully", 
        elapsed=elapsed, 
        data={ "products": data, 
            "page": page, 
            "limit": limit
    } 
) 
    return jsonify(api_response.to_dict()), 200

@product_blueprint.route("/products/inactive", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 1,
            "example": 1
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 10,
            "example": 10
        }
    ],

    "responses": {

        200: {
            "description": "Inactive products retrieved successfully",
            "schema": {
                "$ref": "#/definitions/ProductListResponse"
            }
        },
        400:{
            "description": "Invalid pagination parameters",
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

        500: {
            "description": "Internal server error",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        503: {
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})

def get_inactive_products():

    logger.info("GET /products/inactive")
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        
    except (TypeError, ValueError) as e:
        raise InvalidProductDataError(
            "Page and limit must be integers"
        ) from e

    if page < 1:
        raise InvalidProductDataError(
            "Page must be greater than zero"
        )

    if limit < 1:
        raise InvalidProductDataError(
            "Limit must be greater than zero"
        )


    service = get_service()

    products = service.get_inactive_products(page, limit)

    data = [
        ProductResponseDto(**p).model_dump()
        for p in products
    ]

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Inactive products retrieved successfully",
        elapsed=elapsed,
        data={
            "products": data,
            "page": page,
            "limit": limit
        }
    )

    return jsonify(api_response.to_dict()), 200


@product_blueprint.route("/products/<product_id>", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        }
    ],

    "responses": {

        200: {
            "description": "Product retrieved successfully",
            "schema": {
                "$ref": "#/definitions/ProductResponse"
            }
            
        },

        401: {
            "description": "Unauthorized",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        404: {
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def get_product(product_id):

    logger.info(f"GET /products/{product_id}")

    service = get_service()

    product = service.get_product_by_id(product_id)

    response = ProductResponseDto(**product)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Product found",
        elapsed=elapsed,
        data=response.model_dump()
    )

    return jsonify(api_response.to_dict()), 200


@product_blueprint.route("/internal/products/<product_id>", methods=["GET"])
@swag_from({
    "tags": ["Internal Product"],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        }
    ],

    "responses": {

        200: {
            "description": "Product retrieved successfully",
            "schema": {
                "$ref": "#/definitions/ProductResponse"
            }
        },

        404: {
            "description": "Product not found",
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
def internal_get_product(product_id):
    
    logger.info(f"INTERNAL GET /products/{product_id}")

    service = get_service()

    product = service.get_product_by_id(product_id)
    response = ProductResponseDto(**product)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Product found",
        elapsed=elapsed,
        data=response.model_dump()
    )

    return jsonify(api_response.to_dict()), 200



@product_blueprint.route("/products/<product_id>", methods=["PUT"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "consumes": ["application/json"],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
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
                        "example": "Notebook Dell"
                    },
                    "description": {
                        "type": "string",
                        "example": "Notebook atualizado"
                    },
                    "price": {
                        "type": "number",
                        "format": "float",
                        "example": 3600.00
                    },
                    "quantity": {
                        "type": "integer",
                        "example": 8
                    }
                },
                "required": [
                    "name",
                    "price",
                    "quantity"
                ]
            }
        }
    ],

    "responses": {

        200: {
            "description": "Product updated successfully",
            "schema": {
                "$ref": "#/definitions/ProductResponse"
            }
        },

        400: {
            "description": "Invalid product data",
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
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def update_product(product_id):

    logger.info(f"PUT /products/{product_id}")

    dto = ProductRequestDto(**request.json)

    service = get_service()

    product= service.update_product(product_id, dto)
    
    response = ProductResponseDto(**product)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Product updated successfully",
        elapsed=elapsed,
        data=response.model_dump()
    )

    return jsonify(api_response.to_dict()), 200



@product_blueprint.route("/products/<product_id>", methods=["DELETE"])
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        }
    ],

    "responses": {

        200: {
            "description": "Product deleted successfully",
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
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def delete_product(product_id):

    logger.info(f"DELETE /products/{product_id}")

    service = get_service()

    service.delete_product(product_id)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Product deleted successfully",
        elapsed=elapsed
    )

    return jsonify(api_response.to_dict()), 200


@product_blueprint.route(
    "/products/<product_id>/decrease-stock",
    methods=["PATCH"]
)
@token_required
@swag_from({
    "tags": ["Product"],

    "security": [
        {
            "Bearer": []
        }
    ],

    "consumes": ["application/json"],

    "parameters": [

        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        },

        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "example": 2
                    }
                },
                "required": [
                    "quantity"
                ]
            }
        }
    ],

    "responses": {

        200: {
            "description": "Stock updated successfully",
            "schema": {
                "$ref": "#/definitions/MessageResponse"
            }
        },

        400: {
            "description": "Invalid quantity",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        409: {
            "description": "Insufficient stock",
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
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def decrease_stock(product_id):

    logger.info(
        f"PATCH /products/{product_id}/decrease-stock"
    )

    dto = DecreaseStockDto(**request.json)

    service = get_service()

    service.decrease_stock(
        product_id,
        dto.quantity
    )

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Stock updated successfully",
        elapsed=elapsed
    )

    return jsonify(api_response.to_dict()), 200

@product_blueprint.route(
    "/internal/products/<product_id>/decrease-stock",
    methods=["PATCH"]
)
@swag_from({
    "tags": ["Internal Product"],

    "consumes": ["application/json"],

    "parameters": [

        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        },

        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "example": 2
                    }
                },
                "required": [
                    "quantity"
                ]
            }
        }
    ],

    "responses": {

        200: {
            "description": "Stock updated successfully",
            "schema": {
                "$ref": "#/definitions/MessageResponse"
            }
        },

        400: {
            "description": "Invalid quantity",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },
        409: {
            "description": "Insufficient stock",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        404: {
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def internal_decrease_stock(product_id):

    logger.info(
        f"INTERNAL PATCH /products/{product_id}/decrease-stock"
    )

    dto = DecreaseStockDto(**request.json)

    service = get_service()

    service.decrease_stock(
        product_id,
        dto.quantity
    )

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Stock updated successfully",
        elapsed=elapsed
)

    return jsonify(api_response.to_dict()), 200
    
@product_blueprint.route(
    "/internal/products/<product_id>/increase-stock",
    methods=["PATCH"]
)
@swag_from({
    "tags": ["Internal Product"],

    "consumes": ["application/json"],

    "parameters": [

        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        },

        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "example": 2
                    }
                },
                "required": [
                    "quantity"
                ]
            }
        }
    ],

    "responses": {

        200: {
            "description": "Stock increased successfully",
            "schema": {
                "$ref": "#/definitions/MessageResponse"
            }
        },

        400: {
            "description": "Invalid quantity",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        },

        404: {
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def internal_increase_stock(product_id):

    logger.info(
        f"INTERNAL PATCH /products/{product_id}/increase-stock"
    )

    dto = DecreaseStockDto(**request.json)

    service = get_service()

    service.increase_stock(
        product_id,
        dto.quantity
    )

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Stock increased successfully",
        elapsed=elapsed
    )

    return jsonify(api_response.to_dict()), 200


@product_blueprint.route(
    "/internal/products/<product_id>/stock",
    methods=["GET"]
)
@swag_from({
    "tags": ["Internal Product"],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        }
    ],

    "responses": {

        200: {
            "description": "Current product stock",
            "schema": {
                "$ref": "#/definitions/StockResponse"
            }
            
        },

        404: {
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def internal_get_stock(product_id):

    service = get_service()

    product = service.get_product_by_id(product_id)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Stock found",
        elapsed=elapsed,
        data={
            "quantity": product["quantity"]
        }
    )

    return jsonify(api_response.to_dict()), 200

@product_blueprint.route(
    "/internal/products/<product_id>/price",
    methods=["GET"]
)
@swag_from({
    "tags": ["Internal Product"],

    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "string",
            "required": True,
            "example": "01K2ABC123XYZ"
        }
    ],

    "responses": {

        200: {
            "description": "Current product price",
            "schema": {
                "$ref": "#/definitions/PriceResponse"
            }
            
        },

        404: {
            "description": "Product not found",
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
            "description": "Service unavailable",
            "schema": {
                "$ref": "#/definitions/ErrorResponse"
            }
        }
    }
})
def internal_get_price(product_id):

    service = get_service()

    product = service.get_product_by_id(product_id)

    elapsed = int(
    (time.perf_counter() - g.start_time) * 1000
)

    api_response = ApiResponse(
        message="Price found",
        elapsed=elapsed,
        data={
            "price": product["price"]
        }
    )

    return jsonify(api_response.to_dict()), 200