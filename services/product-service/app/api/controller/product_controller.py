from flask import Blueprint, request, jsonify
from pydantic import ValidationError


from api.dto.response.product_response_dto import ProductResponseDto
from api.dto.request.decrease_stock_dto import DecreaseStockDto
from api.dto.request.product_request_dto import ProductRequestDto

from infrastructure.repositories.product_repository import ProductRepository
from application.service.product_service import ProductService
from infrastructure.logging.logger import get_logger
from infrastructure.security.auth_middleware import token_required
from infrastructure.errors.service_errors import (
ProductNotFoundError,
InvalidProductDataError,
InsufficientStockError,
DatabaseUnavailableError)

product_blueprint = Blueprint("product", __name__)


logger = get_logger(__name__)

def get_service():
    repository = ProductRepository()
    return ProductService(repository)

@product_blueprint.route("/products", methods=["POST"])
@token_required
def create_product():
    try:
        logger.info("POST /products")
        dto = ProductRequestDto(**request.json)
        service = get_service()
        
        #  pegar o usuario por token 
        user = request.user
        user_id = user["client_id"]
        
        product = service.create_product(dto, user_id)

        response = ProductResponseDto(**product)

        return jsonify(response.model_dump()), 201

    except ValidationError as e:
        return jsonify(e.errors()), 400

    except InvalidProductDataError as e:
        return jsonify({"error": str(e)}), 400

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500



@product_blueprint.route("/products", methods=["GET"])
@token_required
def get_all_products():
    try:
        logger.info("GET /products")

        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        
        service = get_service()
        products = service.get_all_products(page, limit)

        data = [
            ProductResponseDto(**p).model_dump()
            for p in products
        ]

        return jsonify({
            "success": True,
            "data": data,
            "page": page,
            "limit": limit
        }), 200

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@product_blueprint.route("/products/<product_id>", methods=["GET"])
@token_required
def get_product(product_id):
    try:
        logger.info(f"GET /products/{product_id}")

        service = get_service()
        product = service.get_product_by_id(product_id)
        response = ProductResponseDto(**product)

        return jsonify(response.model_dump()), 200

    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@product_blueprint.route("/internal/products/<product_id>", methods=["GET"])
def internal_get_product(product_id):
    try:
        logger.info(f"INTERNAL GET /products/{product_id}")

        service = get_service()
        product = service.get_product_by_id(product_id)

        return jsonify(product), 200

    except ProductNotFoundError:
        return jsonify({"error": "Product not found"}), 404

    except Exception as e:
        logger.error(f"Internal error: {e}")
        return jsonify({"error": "Internal server error"}), 500
@product_blueprint.route("/products/<product_id>", methods=["PUT"])
@token_required
def update_product(product_id):
    try:
        logger.info(f"PUT /products/{product_id}")

        dto = ProductRequestDto(**request.json)
        
        service = get_service()
        service.update_product(product_id, dto)

        return jsonify({"message": "Product updated"}), 200

    except ValidationError as e:
        return jsonify(e.errors()), 400

    except InvalidProductDataError as e:
        return jsonify({"error": str(e)}), 400

    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500



@product_blueprint.route("/products/<product_id>", methods=["DELETE"])
@token_required
def delete_product(product_id):
    try:
        logger.info(f"DELETE /products/{product_id}")
        
        service = get_service()
        service.delete_product(product_id)

        return jsonify({"message": "Product deleted"}), 200

    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500



@product_blueprint.route("/products/<product_id>/decrease-stock", methods=["PATCH"])
@token_required
def decrease_stock(product_id):
    try:
        logger.info(f"PATCH /products/{product_id}/decrease-stock")

        dto = DecreaseStockDto(**request.json)
        
        service = get_service()
        service.decrease_stock(product_id, dto.quantity)

        return jsonify({
            "message": "Stock updated"
        }), 200
        
    except ValidationError as e:
        return jsonify(e.errors()), 400

    except InvalidProductDataError as e:
        return jsonify({"error": str(e)}), 400

    except InsufficientStockError as e:
        return jsonify({"error": str(e)}), 400

    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    
@product_blueprint.route(
    "/internal/products/<product_id>/decrease-stock",
    methods=["PATCH"]
)
def internal_decrease_stock(product_id):
    try:
        logger.info(f"INTERNAL PATCH /products/{product_id}/decrease-stock")

        dto = DecreaseStockDto(**request.json)

        service = get_service()
        service.decrease_stock(product_id, dto.quantity)

        return jsonify({
            "message": "Stock updated"
        }), 200

    except InvalidProductDataError as e:
        return jsonify({"error": str(e)}), 400

    except InsufficientStockError as e:
        return jsonify({"error": str(e)}), 400

    except ProductNotFoundError:
        return jsonify({"error": "Product not found"}), 404

    except DatabaseUnavailableError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logger.error(f"Internal error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@product_blueprint.route("/internal/products/<product_id>/stock", methods=["GET"])
def internal_get_stock(product_id):
    service = get_service()
    product = service.get_product_by_id(product_id)

    return jsonify({
        "quantity": product["quantity"]
    }), 200
    
@product_blueprint.route("/internal/products/<product_id>/price", methods=["GET"])
def internal_get_price(product_id):
    service = get_service()
    product = service.get_product_by_id(product_id)

    return jsonify({
        "price": product["price"]
    }), 200