# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Variables de entorno
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]


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


# ==============================================
# scripts/seed_data.py - Script para datos de prueba
# ==============================================
#!/usr/bin/env python3
#"""
#Script para insertar datos de prueba
#Uso: python scripts/seed_data.py
#"""
import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta
import random
from app import create_app, db
from app.models import User, Node, Sensor, Measurement

def seed_database():
    """Inserta datos de prueba"""
    app = create_app('development')
    
    with app.app_context():
        print("Insertando datos de prueba...")
        
        # Crear nodos
        nodes_data = [
            {'ubicacion': 'Laboratorio A - Piso 1', 'microcontrolador': 'ESP32'},
            {'ubicacion': 'Oficina Principal - Piso 2', 'microcontrolador': 'ESP32'},
            {'ubicacion': 'Sala de Servidores - Sótano', 'microcontrolador': 'ESP32'}
        ]
        
        nodes = []
        for node_data in nodes_data:
            existing = Node.query.filter_by(ubicacion=node_data['ubicacion']).first()
            if not existing:
                node = Node(**node_data)
                db.session.add(node)
                nodes.append(node)
        
        db.session.commit()
        print(f"✓ {len(nodes)} nodos creados")
        
        # Crear sensores para cada nodo
        all_nodes = Node.query.all()
        for node in all_nodes:
            if node.sensores.count() == 0:
                sensors = [
                    {
                        'sensor': 'DHT22',
                        'variable': 'temp',
                        'umbral_min': 18.0,
                        'umbral_max': 26.0
                    },
                    {
                        'sensor': 'DHT22',
                        'variable': 'hum',
                        'umbral_min': 30.0,
                        'umbral_max': 70.0
                    },
                    {
                        'sensor': 'MQ-135',
                        'variable': 'CO2',
                        'umbral_min': 300.0,
                        'umbral_max': 1000.0
                    }
                ]
                
                for sensor_data in sensors:
                    sensor = Sensor(nodo_id=node.id, **sensor_data)
                    db.session.add(sensor)
        
        db.session.commit()
        print("✓ Sensores creados")
        
        # Crear usuarios de prueba
        users_data = [
            {
                'nombre': 'Juan Pérez',
                'correo': 'juan@sistema.com',
                'rol': 'usuario',
                'nodo_id': all_nodes[0].id if all_nodes else None,
                'ubicacion_asignada': all_nodes[0].ubicacion if all_nodes else None
            },
            {
                'nombre': 'María García',
                'correo': 'maria@sistema.com',
                'rol': 'usuario',
                'nodo_id': all_nodes[1].id if len(all_nodes) > 1 else None,
                'ubicacion_asignada': all_nodes[1].ubicacion if len(all_nodes) > 1 else None
            }
        ]
        
        for user_data in users_data:
            existing = User.query.filter_by(correo=user_data['correo']).first()
            if not existing:
                user = User()
                user.nombre = user_data['nombre']
                user.correo = user_data['correo']
                user.rol = user_data['rol']
                user.nodo_id = user_data['nodo_id']
                user.ubicacion_asignada = user_data['ubicacion_asignada']
                user.set_password('Usuario123!')
                db.session.add(user)
        
        db.session.commit()
        print("✓ Usuarios de prueba creados (contraseña: Usuario123!)")
        
        # Crear mediciones de prueba (últimas 24 horas)
        print("Creando mediciones de prueba...")
        for node in all_nodes:
            base_time = datetime.utcnow() - timedelta(hours=24)
            
            for i in range(48):  # Una medición cada 30 minutos
                measurement = Measurement(
                    nodo_id=node.id,
                    fecha_hora=base_time + timedelta(minutes=30*i),
                    temperatura=random.uniform(20, 25),
                    humedad=random.uniform(40, 60),
                    co2=random.uniform(400, 800)
                )
                db.session.add(measurement)
        
        db.session.commit()
        print("✓ Mediciones de prueba creadas")
        
        print("\n=== RESUMEN ===")
        print(f"Nodos: {Node.query.count()}")
        print(f"Sensores: {Sensor.query.count()}")
        print(f"Usuarios: {User.query.count()}")
        print(f"Mediciones: {Measurement.query.count()}")
        print("\n✓ Base de datos inicializada con datos de prueba")

if __name__ == '__main__':
    seed_database()