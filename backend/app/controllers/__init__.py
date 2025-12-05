# backend/app/blueprints/__init__.py
from flask import Blueprint

def register_blueprints(app):
    """Registra todos los blueprints"""
    from app.controllers.auth import auth_bp
    from app.controllers.users import users_bp
    from app.controllers.nodes import nodes_bp
    from app.controllers.measurements import measurements_bp
    from app.controllers.alerts import alerts_bp
    from app.controllers.reports import reports_bp
    from app.controllers.iot import iot_bp
    
    
   # from app.blueprints.web import web_bp # Lo comentamos por ahora (ver nota abajo)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(nodes_bp, url_prefix='/api/nodes')
    app.register_blueprint(measurements_bp, url_prefix='/api/measurements')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(iot_bp, url_prefix='/api/iot')
    # app.register_blueprint(web_bp)