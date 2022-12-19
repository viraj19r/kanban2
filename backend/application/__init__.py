from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
app = None

def create_app():
    # set the location of templates and static folder manually
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    app.config.from_object(LocalDevelopmentConfig) # configure the basic config setting fron config.py
    db.init_app(app)
    app.app_context().push() # push app context beyond the context of this app so that database can access it
    return app


app = create_app()

from application.api import *
from application.controllers import *