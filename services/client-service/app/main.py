import time
from flask import Flask, g
from flasgger import Swagger 
from api.controller.client_controller import client_bp
from api.controller.auth_controller import auth_bp
from api.middleware.exception_middleware import register_exception_handlers
from api.swagger.schemas import (
    CLIENT_SCHEMA,
    CLIENT_RESPONSE_SCHEMA,
    CLIENT_LIST_RESPONSE_SCHEMA,
    MESSAGE_RESPONSE_SCHEMA,
    LOGIN_RESPONSE_SCHEMA,
    ERROR_RESPONSE_SCHEMA
)

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Client API',
    'uiversion': 3
}

swagger_template = {
    "swagger": "2.0",

    "info": {
        "title": "Client API",
        "description": "API responsible for client management",
        "version": "1.0.0"
    },

    "securityDefinitions": {

        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Digite: Bearer <seu_token>"
        }
    },

    "definitions": {

        "Client": CLIENT_SCHEMA,

        "ClientResponse": CLIENT_RESPONSE_SCHEMA,

        "ClientListResponse": CLIENT_LIST_RESPONSE_SCHEMA,

        "MessageResponse": MESSAGE_RESPONSE_SCHEMA,

        "LoginResponse": LOGIN_RESPONSE_SCHEMA,

        "ErrorResponse": ERROR_RESPONSE_SCHEMA

    }

}

Swagger(
    app,
    template=swagger_template
)


@app.before_request
def start_request_timer():
    """
    Starts the timer for every HTTP request.

    The value is stored in Flask's request-local context
    and is used to calculate the total request elapsed time.
    """
    g.start_time = time.perf_counter()

@app.route("/")
def home():
    return {"message": "API do Client Service rodando"}

register_exception_handlers(app)
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)

if __name__ =="__main__":
    app.run(
        host = "0.0.0.0",
        port= 5000,
        debug=False,
        ) 