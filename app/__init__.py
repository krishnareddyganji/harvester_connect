from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import pymysql

# Fix MySQL import issue
pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Models import inside app context to avoid circular import
    with app.app_context():
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Register Blueprints
        from .routes.auth import auth
        from .routes.user import user
        from .routes.admin import admin
        from .routes.main import main
        from .routes.owner import owner_bp
        from .routes.search import search_bp

        app.register_blueprint(auth)
        app.register_blueprint(user)
        app.register_blueprint(admin, url_prefix='/admin')
        app.register_blueprint(main)
        app.register_blueprint(owner_bp)
        app.register_blueprint(search_bp)

    return app
