import os
from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'hwalloc.sqlite'),
        DEVICE_OVERSUBSCRIBE=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else: 
        # load the test cofnig if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import devices
    app.register_blueprint(devices.bp)
    app.add_url_rule('/', endpoint='index'
    )

    from . import api
    app.register_blueprint(api.bp)
    return app