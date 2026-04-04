from flask import Flask
from flasgger import Swagger
from api.controller.client_controller import client_bp

app = Flask(__name__)
Swagger(app)

@app.route("/")
def home():
    return {"messege": "API do Client Service rodando"}

app.register_blueprint(client_bp)
if __name__ =="__main__":
    app.run(debug=True, use_reloader=False) 