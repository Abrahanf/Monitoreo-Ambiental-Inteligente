# backend/app/services/node_service.py
from app.repositories import NodeRepository

class NodeService:
    @staticmethod
    def create_node(data):
        """Crea un nuevo nodo"""
        node = NodeRepository.create(data)
        return {'node': node.to_dict(), 'message': 'Nodo creado exitosamente'}, 201
    
    @staticmethod
    def get_node(node_id):
        """Obtiene un nodo por ID"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        return {'node': node.to_dict()}, 200
    
    @staticmethod
    def get_all_nodes():
        """Obtiene todos los nodos"""
        nodes = NodeRepository.find_all()
        return {'nodes': [n.to_dict() for n in nodes]}, 200
    
    @staticmethod
    def update_node(node_id, data):
        """Actualiza un nodo"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        node = NodeRepository.update(node_id, data)
        return {'node': node.to_dict(), 'message': 'Nodo actualizado'}, 200
    
    @staticmethod
    def delete_node(node_id):
        """Elimina un nodo"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        NodeRepository.delete(node_id)
        return {'message': 'Nodo eliminado exitosamente'}, 200
    
    @staticmethod
    def add_sensor(node_id, sensor_data):
        """Agrega un sensor a un nodo"""
        node = NodeRepository.find_by_id(node_id)
        if not node:
            return {'error': 'Nodo no encontrado'}, 404
        
        sensor = NodeRepository.add_sensor(node_id, sensor_data)
        return {'sensor': sensor.to_dict(), 'message': 'Sensor agregado'}, 201
    
    @staticmethod
    def update_sensor(sensor_id, sensor_data):
        """Actualiza un sensor"""
        sensor = NodeRepository.update_sensor(sensor_id, sensor_data)
        if not sensor:
            return {'error': 'Sensor no encontrado'}, 404
        return {'sensor': sensor.to_dict(), 'message': 'Sensor actualizado'}, 200
    
    @staticmethod
    def delete_sensor(sensor_id):
        """Elimina un sensor"""
        sensor = NodeRepository.delete_sensor(sensor_id)
        if not sensor:
            return {'error': 'Sensor no encontrado'}, 404
        return {'message': 'Sensor eliminado'}, 200
