from flask import Flask
from flasgger import Swagger
from api.config import SWAGGER
from api.mae_api import mae_api
from api.filha_api import filha_api

app = Flask(__name__)
app.config["SWAGGER"] = SWAGGER

swagger = Swagger(app)

# Registrar as blueprints
app.register_blueprint(mae_api, url_prefix="/api")
app.register_blueprint(filha_api, url_prefix="/api")
