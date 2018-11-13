from flask import Flask
from flask_bootstrap import Bootstrap

def create_app(config_filename=None):

    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_object('config.default')

    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py', silent=True)

    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    app.config.from_envvar('APP_CONFIG_FILE')

    # TODO: Override with variables passed in - needed? test overrides?
    #app.config.from_pyfile(config_filename)

    from . import db
    db.init_app(app)

    from .views.views import views
    app.register_blueprint(views)

    Bootstrap(app)

    return app
