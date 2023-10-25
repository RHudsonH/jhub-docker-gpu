import os
from flask import Flask

def create_app(test_config=None):
    # If this environment variable isn't set Flask will revert to its default behavior.
    instance_path_env = os.environ.get('FLASK_INSTANCE_PATH')
    config_file = os.environ.get('FLASK_CONFIG_FILE') or 'config.py'
    
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path_env)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'hwalloc.sqlite'),
        DEVICE_OVERSUBSCRIBE=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(config_file, silent=True)
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

    from . import healthz
    app.register_blueprint(healthz.bp)

    return app
