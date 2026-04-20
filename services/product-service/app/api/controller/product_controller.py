from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from api.dto.request.product_request_dto import ProductRequestDto
from api.dto.response.product_response_dto import ProductResponseDto

from infrastructure.repositories.product_repository import ProductRepository
from application.service.product_service import ProductService

from infrastructure.logging.logger import logger

product_blueprint = Blueprint("product", __name__)

repository = ProductRepository()
service = ProductService(repository)


@product_blueprint.route("/products", methods=["POST"])
def create_product():
    """
    Criar um novo produto
    ---
    tags:
      - Products
    parameters:
      - in: body
        name: product
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Nome do Produto
            description:
              type: string
              example: Descrição do Produto
            price:
              type: number
              example: 3500
            quantity:
              type: integer
              example: 10
    responses:
      201:
        description: Produto criado com sucesso
      400:
        description: Erro de validação
      500:
        description: Erro interno
    """
    try:
        logger.info("POST /products")

        dto = ProductRequestDto(**request.json)
        product = service.create_product(dto)

        response = ProductResponseDto(**product)

        return jsonify(response.dict()), 201

    except ValidationError as e:
        logger.warning(f"Validation Error: {e}")
        return jsonify(e.errors()), 400

    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500


@product_blueprint.route("/products", methods=["GET"])
def get_all_products():
    """
    Listar todos os produtos
    ---
    tags:
      - Products
    responses:
      200:
        description: Lista de produtos
    """
    try:
        logger.info("GET /products")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        products = service.get_all_products(page, limit)
        response = [ProductResponseDto(**p).dict() for p in products]

        return jsonify({
            "success": True,
            "data": products,
            "page": page,
            "limit": limit}), 200

    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"error": str(e)}), 500


@product_blueprint.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    """
    Buscar produto por ID
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        required: true
        schema:
          type: string
    responses:
      200:
        description: Produto encontrado
      404:
        description: Produto não encontrado
    """
    try:
        logger.info(f"GET /products/{product_id}")

        product = service.get_product_by_id(product_id)
        response = ProductResponseDto(**product)

        return jsonify(response.dict()), 200

    except Exception as e:
        logger.error(f"Error fetching product: {e}")
        return jsonify({"error": str(e)}), 404


@product_blueprint.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Atualizar produto
    
    ---
    
    tags:
      - Products
    consumes:
      - application/json
    parameters:
      - name: product_id
        in: path
        required: true
        type: string

      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
            quantity:
              type: integer

    responses:
      200:
        description: Produto atualizado
      400:
        description: Erro de validação
"""
    try:
        logger.info(f"PUT /products/{product_id}")
        
        dto = ProductRequestDto(**request.json)
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
    """
    Deletar (desativar) produto
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        required: true
        schema:
          type: string
    responses:
      200:
        description: Produto deletado
    """
    try:
        logger.info(f"DELETE /products/{product_id}")

        service.delete_product(product_id)

        return jsonify({"message": "Product deleted"}), 200

    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({"error": str(e)}), 400