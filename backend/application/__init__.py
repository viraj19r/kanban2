from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import *
from application import workers
from flask_caching import Cache
app = None
celery = None
cache = None
def create_app():
    # set the location of templates and static folder manually
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    CORS(app)
    app.config.from_object(LocalDevelopmentConfig) # configure the basic config setting fron config.py
    db.init_app(app)
    app.app_context().push() # push app context beyond the context of this app so that database can access it
    #create celery
    celery = workers.celery

    # update configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        enable_utc = False
    )

    celery.Task = workers.ContextTask
    cache = Cache(app)
    app.app_context().push()
    return app, celery, cache


app, celery,cache = create_app()
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
Security(app, user_datastore)

from application.api import *
from application.controllers import *


db.create_all()