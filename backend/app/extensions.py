# backend/app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Inicializar extensiones
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()

def init_extensions(app):
    """Inicializa todas las extensiones"""
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)
    bcrypt.init_app(app)
