from flask import Flask
from flask_webpack import Webpack
from app.database import mongo, ora
from app.controllers.GithubController import githubBlueprint
from app.controllers.StackoverflowController import stackoverflowBlueprint
from app.controllers.RatingController import ratingBlueprint
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from werkzeug.contrib.fixers import ProxyFix


from flask_dance.contrib.github import make_github_blueprint

app = Flask(__name__)

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=find_dotenv())

app.secret_key = os.getenv('SECRET_KEY')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.register_blueprint(githubBlueprint)
app.register_blueprint(projectBlueprint)
app.register_blueprint(stackoverflowBlueprint)
app.register_blueprint(ratingBlueprint)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

webpack = Webpack()

app.config["WTF_CSRF_ENABLED"]=True
app.config["MONGODB_SETTINGS"] = {
    'db': 'cowork',
    'host': '127.0.0.1',
    'port': 27017
}

app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
app.config["MONGODB_PORT"] =os.getenv("MONGODB_PORT")
app.config["REDIS_HOST"] = os.getenv("REDIS_HOST")
app.config["REDIS_PORT"] = os.getenv("REDIS_PORT")

app.config["WEBPACK_MANIFEST_PATH"] = os.getenv("WEBPACK_MANIFEST")
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")

app.config['ORATOR_DATABASES'] = {
    'mysql': {
        'driver':  os.getenv("DB"),
        'database':  os.getenv("DB_DATABASE"),
        "password":  os.getenv("DB_PASSWORD"),
        "host":  os.getenv("DB_HOST"),
        "user":  os.getenv("DB_USER"),
        "port":  int(os.getenv("DB_PORT"))
    }
}

app.config["STACKOVERFLOW_CLIENT_ID"]= os.getenv("STACKOVERFLOW_CLIENT_ID")
app.config["STACKOVERFLOW_CLIENT_SECRET"]=os.getenv("STACKOVERFLOW_CLIENT_SECRET")
app.config["STACKOVERFLOW_KEY"]= os.getenv("STACKOVERFLOW_KEY")
app.config["STACKOVERFLOW_SCOPE"]= os.getenv("STACKOVERFLOW_SCOPE")
app.config["STACKOVERFLOW_REDIRECT_URI"]= os.getenv("STACKOVERFLOW_REDIRECT_URI")

blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
)
app.register_blueprint(blueprint, url_prefix="/login")


mongo.init_app(app)
ora.init_app(app)

webpack.init_app(app)