from flask import Flask
from flasgger import Swagger
from api.controller.client_controller import client_bp
from api.controller.auth_controller import auth_bp

app = Flask(__name__)
Swagger(app)

@app.route("/")
def home():
    return {"messege": "API do Client Service rodando"}

app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
if __name__ =="__main__":
    app.run(
        host = "0.0.0.0",
        port= 5000,
        debug=False,
        ) 