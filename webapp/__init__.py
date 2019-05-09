import logging
from flask import Flask, has_request_context, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_celery import Celery
# from flask_caching import Cache
# from flask_mail import Mail
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_assets import Environment, Bundle
# from flask_youtube import Youtube

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
# celery = Celery()
# debug_toolbar = DebugToolbarExtension()
# cache = Cache()
# assets_env = Environment()
# mail = Mail()
# youtube = Youtube()

# main_css = Bundle(
#     'css/bootstrap.css',
#     filters='cssmin',
#     output='css/common.css'
# )

# main_js = Bundle(
#     'js/jquery.js',
#     'js/bootstrap.js',
#     filters='jsmin',
#     output='js/common.js'
# )


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. project.config.ProdConfig
    """
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db)

    from .main import create_module as main_create_module
    from .api import create_module as api_create_module
    from .core import create_module as core_create_module
    main_create_module(app)
    api_create_module(app)
    core_create_module(app)
    return app

