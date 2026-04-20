from flask import Flask
from flasgger import Swagger
from api.controller.product_controller import product_blueprint

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Product API MARIA',
    'uiversion': 3
}

Swagger(app)

app.register_blueprint(product_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)