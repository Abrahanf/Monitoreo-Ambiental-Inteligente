# backend/app/repositories/node_repository.py
from datetime import datetime
from app.extensions import db
from app.models import Node, Sensor

class NodeRepository:
    @staticmethod
    def create(node_data):
        """Crea un nuevo nodo"""
        node = Node(**node_data)
        db.session.add(node)
        db.session.commit()
        return node
    
    @staticmethod
    def find_by_id(node_id):
        """Busca nodo por ID"""
        return Node.query.get(node_id)
    
    @staticmethod
    def find_all():
        """Obtiene todos los nodos"""
        return Node.query.all()
    
    @staticmethod
    def find_active():
        """Obtiene nodos activos"""
        return Node.query.filter_by(estado='ON').all()
    
    @staticmethod
    def update(node_id, node_data):
        """Actualiza un nodo"""
        node = Node.query.get(node_id)
        if node:
            for key, value in node_data.items():
                if hasattr(node, key):
                    setattr(node, key, value)
            db.session.commit()
        return node
    
    @staticmethod
    def delete(node_id):
        """Elimina un nodo"""
        node = Node.query.get(node_id)
        if node:
            db.session.delete(node)
            db.session.commit()
        return node
    
    @staticmethod
    def update_last_connection(node_id):
        """Actualiza última conexión"""
        node = Node.query.get(node_id)
        if node:
            node.ultima_conexion = datetime.utcnow()
            db.session.commit()
        return node
    
    @staticmethod
    def add_sensor(node_id, sensor_data):
        """Agrega un sensor a un nodo"""
        sensor = Sensor(nodo_id=node_id, **sensor_data)
        db.session.add(sensor)
        db.session.commit()
        return sensor
    
    @staticmethod
    def update_sensor(sensor_id, sensor_data):
        """Actualiza un sensor"""
        sensor = Sensor.query.get(sensor_id)
        if sensor:
            for key, value in sensor_data.items():
                if hasattr(sensor, key):
                    setattr(sensor, key, value)
            db.session.commit()
        return sensor
    
    @staticmethod
    def delete_sensor(sensor_id):
        """Elimina un sensor"""
        sensor = Sensor.query.get(sensor_id)
        if sensor:
            db.session.delete(sensor)
            db.session.commit()
        return sensor
