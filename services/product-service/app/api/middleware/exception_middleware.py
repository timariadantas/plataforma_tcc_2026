import time

from flask import jsonify, g
from pydantic import ValidationError

from api.dto.response.api_response import ApiResponse

from infrastructure.errors.service_errors import (
    ProductNotFoundError,
    ProductAlreadyExistsError,
    InvalidProductDataError,
    InsufficientStockError,
    DatabaseUnavailableError,
    AuthenticationError,
    InvalidTokenError,
    ExpiredTokenError,
)


def register_exception_handlers(app):

    @app.errorhandler(ProductNotFoundError)
    def handle_product_not_found(error):
        return _error_response(
            "Product not found",
            str(error),
            404
        )

    @app.errorhandler(ProductAlreadyExistsError)
    def handle_product_already_exists(error):
        return _error_response(
            "Request failed",
            str(error),
            409
        )

    @app.errorhandler(InvalidProductDataError)
    def handle_invalid_product_data(error):
        return _error_response(
            "Request failed",
            str(error),
            400
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return _error_response(
            "Request failed",
            "Invalid product data",
            400
        )

    @app.errorhandler(InsufficientStockError)
    def handle_insufficient_stock(error):
        return _error_response(
            "Request failed",
            str(error),
            409
        )

    @app.errorhandler(DatabaseUnavailableError)
    def handle_database_unavailable(error):
        return _error_response(
            "Request failed",
            str(error),
            503
        )

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        return _error_response(
            "Request failed",
            str(error),
            401
        )

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(error):
        return _error_response(
            "Request failed",
            str(error),
            401
        )

    @app.errorhandler(ExpiredTokenError)
    def handle_expired_token(error):
        return _error_response(
            "Request failed",
            "Token expired",
            401
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return _error_response(
            "Request failed",
            "Internal server error",
            500
        )


def _error_response(message, error, status_code):

    elapsed = int(
        (time.perf_counter() - g.start_time) * 1000
    )

    response = ApiResponse(
        message=message,
        elapsed=elapsed,
        error=error
    )

    return jsonify(response.to_dict()), status_code