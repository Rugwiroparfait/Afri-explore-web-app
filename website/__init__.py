from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Define the name of the database file
DB_NAME = "database.db"

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask app, sets the configuration,
    registers blueprints, and sets up the database and login manager.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Set secret key for session management
    app.config['SECRET_KEY'] = "helloworld"
    
    # Set the database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)
    
    # Import and register the blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    # Import the User model to ensure it is created in the database
    from .models import User
    
    # Create the database if it doesn't exist
    create_database(app)
    
    # Initialize the login manager
    login_manager = LoginManager()
    
    # Set the login view for the login manager
    login_manager.login_view = "auth.login"
    
    # Initialize the login manager with the app
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        """
        Load a user by their ID.

        This function is used by Flask-Login to retrieve a user instance from
        the database by their user ID.

        Args:
            id (int): The user ID.

        Returns:
            User: The user instance corresponding to the given ID.
        """
        return User.query.get(int(id))
    
    return app

def create_database(app):
    """
    Create the database if it doesn't already exist.

    This function checks if the database file exists, and if not,
    it creates the database and all required tables.

    Args:
        app (Flask): The Flask application instance.
    """
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database successfully created!")
