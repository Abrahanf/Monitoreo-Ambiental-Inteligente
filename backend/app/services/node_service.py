# backend/app/services/node_service.py
from app.repositories.node_repository import NodeRepository
# Necesitamos el de sensores para agregar/borrar sensores
from app.repositories.sensor_repository import SensorRepository 

class NodeService:
    def __init__(self):
        # Inyectamos los repositorios
        self.node_repo = NodeRepository()
        self.sensor_repo = SensorRepository()

    def create_node(self, data):
        """Crea un nuevo nodo"""
        # Usamos **data para desempaquetar el diccionario
        node = self.node_repo.create(**data)
        return {'node': node.to_dict(), 'message': 'Nodo creado exitosamente'}, 201
    
    def get_node(self, node_id):
        """Obtiene un nodo por ID"""
        node = self.node_repo.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        # Usamos un to_dict_full si quieres ver sensores, o el normal
        return {'node': node.to_dict()}, 200
    
    def get_all_nodes(self):
        """Obtiene todos los nodos"""
        nodes = self.node_repo.find_all()
        # Aquí puedes incluir los sensores en el dict si quieres mostrarlos en el dashboard
        return {'nodes': [n.to_dict() for n in nodes]}, 200
    
    def update_node(self, node_id, data):
        """Actualiza un nodo"""
        node = self.node_repo.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        node = self.node_repo.update(node_id, data)
        return {'node': node.to_dict(), 'message': 'Nodo actualizado'}, 200
    
    def delete_node(self, node_id):
        """Elimina un nodo"""
        node = self.node_repo.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        self.node_repo.delete(node)
        return {'message': 'Nodo eliminado exitosamente'}, 200
    
    # --- GESTIÓN DE SENSORES ---
    # Usamos el sensor_repo para esto, es más limpio
    
    def add_sensor(self, node_id, sensor_data):
        """Agrega un sensor a un nodo"""
        node = self.node_repo.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        # Aseguramos que el sensor quede ligado al nodo
        sensor_data['nodo_id'] = node_id
        # Asumimos que tu SensorRepository tiene un create similar al de alertas
        sensor = self.sensor_repo.create(**sensor_data)
        
        return {'sensor': sensor.to_dict(), 'message': 'Sensor agregado'}, 201
    
    def update_sensor(self, sensor_id, sensor_data):
        """Actualiza un sensor"""
        # Necesitas implementar update en SensorRepository o usar la lógica aquí
        # Por simplicidad usaremos lógica directa si el repo no tiene update
        from app.models.sensor import Sensor 
        from app.extensions import db
        
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return {'error': 'Sensor no encontrado'}, 404
            
        for key, value in sensor_data.items():
            if hasattr(sensor, key):
                setattr(sensor, key, value)
        db.session.commit()
        
        return {'sensor': sensor.to_dict(), 'message': 'Sensor actualizado'}, 200
    
    def delete_sensor(self, sensor_id):
        """Elimina un sensor"""
        from app.models.sensor import Sensor
        from app.extensions import db
        
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return {'error': 'Sensor no encontrado'}, 404
            
        db.session.delete(sensor)
        db.session.commit()
        
        return {'message': 'Sensor eliminado'}, 200