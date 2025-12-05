# backend/app/repositories/node_repository.py


from datetime import datetime
from app.extensions import db
from app.models.node import Node

class NodeRepository:
    
    def create(self, **kwargs):
        """Crea un nuevo nodo recibiendo argumentos sueltos"""
        node = Node(**kwargs)
        db.session.add(node)
        db.session.commit()
        return node
    
    def find_by_id(self, node_id):
        """Busca nodo por ID"""
        return Node.query.get(node_id)
    
    def find_all(self):
        """Obtiene todos los nodos"""
        return Node.query.all()
    
    def find_active(self):
        """Obtiene nodos activos"""
        return Node.query.filter_by(estado='ON').all()
    
    def update(self, node_id, node_data):
        """Actualiza un nodo"""
        node = Node.query.get(node_id)
        if node:
            for key, value in node_data.items():
                if hasattr(node, key):
                    setattr(node, key, value)
            db.session.commit()
        return node
    
    def delete(self, node):
        """Elimina un nodo (recibe el objeto, no el ID)"""
        # El servicio ya busca el objeto antes de llamar a esto
        db.session.delete(node)
        db.session.commit()
        return node
    
    def update_last_connection(self, node_id):
        """Actualiza última conexión"""
        node = Node.query.get(node_id)
        if node:
            node.ultima_conexion = datetime.utcnow()
            db.session.commit()
        return node

    # NOTA: Los métodos de sensores (add_sensor, etc.) se han movido 
    # a SensorRepository para mantener el orden.