from flask import Blueprint, request, jsonify
from pydantic import ValidationError


from app.api.dto.response.product_response_dto import ProductResponseDto
from app.api.dto.request.decrease_stock_dto import DecreaseStockDto
from app.api.dto.request.product_request_dto import ProductRequestDto

from app.infrastructure.repositories.product_repository import ProductRepository
from app.application.service.product_service import ProductService
from app.infrastructure.logging.logger import get_logger

product_blueprint = Blueprint("product", __name__)


logger = get_logger(__name__)

def get_service():
    repository = ProductRepository()
    return ProductService(repository)

@product_blueprint.route("/products", methods=["POST"])
def create_product():
    try:
        logger.info("POST /products")
        
        service = get_service()
        dto = ProductRequestDto(**request.json)
        product = service.create_product(dto)

        response = ProductResponseDto(**product)

        return jsonify(response.model_dump()), 201

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify(e.errors()), 400

    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500



@product_blueprint.route("/products", methods=["GET"])
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

    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"error": str(e)}), 500


@product_blueprint.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        logger.info(f"GET /products/{product_id}")

        service = get_service()
        product = service.get_product_by_id(product_id)
        response = ProductResponseDto(**product)

        return jsonify(response.model_dump()), 200

    except ValueError as e:
        logger.warning(f"Product not found: {e}")
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        return jsonify({"error": str(e)}), 500


@product_blueprint.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    try:
        logger.info(f"PUT /products/{product_id}")

        dto = ProductRequestDto(**request.json)
        
        service = get_service()
        service.update_product(product_id, dto)

        return jsonify({"message": "Product updated"}), 200

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify(e.errors()), 400

    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return jsonify({"error": str(e)}), 400



@product_blueprint.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        logger.info(f"DELETE /products/{product_id}")
        
        service = get_service()
        service.delete_product(product_id)

        return jsonify({"message": "Product deleted"}), 200

    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({"error": str(e)}), 400



@product_blueprint.route("/products/<product_id>/decrease-stock", methods=["PATCH"])
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
        logger.warning(f"Validation error: {e}")
        return jsonify(e.errors()), 400

    except Exception as e:
        logger.error(f"Error decreasing stock: {e}")
        return jsonify({"error": str(e)}), 400