# backend/app/__init__.py
from flask import Flask
from app.config import config
from app.extensions import init_extensions, db
from app.blueprints import register_blueprints

def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__, 
                template_folder='../../frontend/templates',
                static_folder='../../frontend/static')
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    init_extensions(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Crear tablas en contexto de aplicación
    with app.app_context():
        db.create_all()
    
    return app
