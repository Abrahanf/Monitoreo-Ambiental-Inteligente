# ==============================================
# scripts/init_db.py - Script para inicializar la base de datos
# ==============================================
#!/usr/bin/env python3
#"""
#Script para inicializar la base de datos
#Uso: python scripts/init_db.py
#"""

import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import User, Node, Sensor

def init_database():
    """Inicializa la base de datos"""
    app = create_app('development')
    
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        print("✓ Tablas creadas exitosamente")
        
        # Crear usuario administrador por defecto
        admin = User.query.filter_by(correo='admin@sistema.com').first()
        if not admin:
            admin = User()
            admin.nombre = 'Administrador'
            admin.correo = 'admin@sistema.com'
            admin.rol = 'administrador'
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print(f"✓ Usuario administrador creado: {admin.correo} / Admin123!")
        else:
            print("✓ Usuario administrador ya existe")

if __name__ == '__main__':
    init_database()

