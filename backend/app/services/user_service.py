# backend/app/services/user_service.py
from app.repositories import UserRepository

class UserService:
    @staticmethod
    def create_user(data):
        """Crea un nuevo usuario"""
        # Validar que el correo no exista
        if UserRepository.find_by_email(data['correo']):
            return {'error': 'El correo electrónico ya está en uso'}, 400
        
        # Crear usuario con contraseña temporal
        from app.models import User
        user = User()
        user.nombre = data['nombre']
        user.correo = data['correo']
        user.rol = data.get('rol', 'usuario')
        user.nodo_id = data.get('nodo_id')
        user.ubicacion_asignada = data.get('ubicacion_asignada')
        user.set_password(data.get('contraseña', 'temporal123'))
        
        user = UserRepository.create({
            'nombre': user.nombre,
            'correo': user.correo,
            'contraseña': user.contrasena,
            'rol': user.rol,
            'nodo_id': user.nodo_id,
            'ubicacion_asignada': user.ubicacion_asignada
        })
        
        return {'user': user.to_dict(), 'message': 'Usuario creado exitosamente'}, 201
    
    @staticmethod
    def get_user(user_id):
        """Obtiene un usuario por ID"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        return {'user': user.to_dict()}, 200
    
    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios"""
        users = UserRepository.find_all()
        return {'users': [u.to_dict() for u in users]}, 200
    
    @staticmethod
    def update_user(user_id, data):
        """Actualiza un usuario"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        
        # Si se actualiza el correo, validar que no exista
        if 'correo' in data and data['correo'] != user.correo:
            if UserRepository.find_by_email(data['correo']):
                return {'error': 'El correo electrónico ya está en uso'}, 400
        
        user = UserRepository.update(user_id, data)
        return {'user': user.to_dict(), 'message': 'Usuario actualizado'}, 200
    
    @staticmethod
    def delete_user(user_id, soft_delete=True):
        """Elimina un usuario"""
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        
        UserRepository.delete(user_id, soft_delete)
        return {'message': 'Usuario eliminado exitosamente'}, 200
