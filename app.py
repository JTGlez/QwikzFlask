import os
from flask import Flask
from flask_cors import CORS, cross_origin
from routes.auth import bp as auth_blueprint
from routes.students import bp as students_blueprint

# Init Flask application as an instance from the Flask class using factory pattern
def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Development configs
    app.config.from_mapping(
        SECRET_KEY='SECRET KEY!',
        DATABASE_URL=os.environ.get('DATABASE_URL')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Register the blueprints for the app
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(students_blueprint)

    # A root page that says hello
    @app.route('/')
    def root():
        return '<h1>Root Page</h1>'

    # A simple page that says hello
    @app.route('/hello')
    @cross_origin()
    def hello():
        return 'Hello, World from Cross-Origin Resource Sharing!'

    # Return the created app
    return app