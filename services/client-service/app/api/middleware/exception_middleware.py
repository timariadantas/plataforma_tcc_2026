import time

from flask import jsonify, g

from api.dto.api_response import ApiResponse

from infrastructure.errors.service_errors import (
    ValidationError,
    DatabaseUnavailableError,
    ClientNotFoundError,
    ClientEmailAlreadyExistsError,
    AuthenticationError
)


def register_exception_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return _error_response(
            "Request failed",
            str(error),
            400
        )

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        return _error_response(
            "Request failed",
            str(error),
            401
        )

    @app.errorhandler(ClientNotFoundError)
    def handle_client_not_found(error):
        return _error_response(
            "Request failed",
            str(error),
            404
        )

    @app.errorhandler(ClientEmailAlreadyExistsError)
    def handle_email_already_exists(error):
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