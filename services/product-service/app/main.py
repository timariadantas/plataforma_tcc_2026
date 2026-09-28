import time
from flask import Flask, g
from flasgger import Swagger
from api.controller.product_controller import product_blueprint
from api.middleware.exception_middleware import register_exception_handlers
from api.swagger.schemas import (
    PRODUCT_SCHEMA,
    PRODUCT_RESPONSE_SCHEMA,
    PRODUCT_LIST_RESPONSE_SCHEMA,
    MESSAGE_RESPONSE_SCHEMA,
    STOCK_RESPONSE_SCHEMA,
    PRICE_RESPONSE_SCHEMA,
    ERROR_RESPONSE_SCHEMA
)

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Product API ',
    'uiversion': 3
}
swagger_template = {
    "swagger": "2.0",

    "info": {
        "title": "Product API",
        "description": "API responsible for product management",
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

        "Product": PRODUCT_SCHEMA,

        "ProductResponse": PRODUCT_RESPONSE_SCHEMA,

        "ProductListResponse": PRODUCT_LIST_RESPONSE_SCHEMA,

        "MessageResponse": MESSAGE_RESPONSE_SCHEMA,

        "StockResponse": STOCK_RESPONSE_SCHEMA,

        "PriceResponse": PRICE_RESPONSE_SCHEMA,
        
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





app.register_blueprint(product_blueprint)
register_exception_handlers(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)