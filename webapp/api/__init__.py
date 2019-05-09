from flask_restful import Api
from .extractor.controllers import extractor_blueprint
from .annotation.controllers import annotation_blueprint


def create_module(app, **kwargs):
    app.register_blueprint(extractor_blueprint)
    app.register_blueprint(annotation_blueprint)