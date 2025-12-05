from flask import Flask
from flask_cors import CORS  # <--- IMPORTANTE: Importar CORS
from flask_jwt_extended import JWTManager
from app.config import config
from app.extensions import db, migrate # Importamos extensiones directas
from app.controllers import register_blueprints

def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    # 1. Crear App
    app = Flask(__name__)
    
    # 2. Cargar Configuración
    app.config.from_object(config[config_name])
    
    # 3. HABILITAR CORS (ESTO ES LO QUE TE FALTA)
    # Permite que el puerto 3000 (React) pida datos al 5000 (Flask)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 4. Inicializar Extensiones
    # Puedes usar tu función init_extensions(app) si prefieres, 
    # pero asegurate de que inicialice db y migrate. 
    # Aquí lo hago explícito para asegurar que funcione:
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    
    # 5. Registrar Blueprints (Rutas)
    register_blueprints(app)
    
    return app