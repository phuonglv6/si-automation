def create_module(app, **kwargs):
    from .filters import core_blueprint
    app.register_blueprint(core_blueprint)