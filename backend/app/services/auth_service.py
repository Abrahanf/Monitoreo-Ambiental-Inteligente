# backend/app/services/auth_service.py
from flask_jwt_extended import create_access_token, create_refresh_token
from app.repositories import UserRepository
from werkzeug.security import check_password_hash, generate_password_hash

class AuthService:
   
    def __init__(self):
        self.user_repo = UserRepository()
    def login(self, email, password):
        """Autentica un usuario y genera tokens JWT"""
        user = self.user_repo.find_by_email(email)
        
        if not user:
            return {'error': 'Correo o contraseña inválidos'}, 401
        
        if not user.activo:
            return {'error': 'Usuario inactivo'}, 403
        
        if not user.check_password(password):
            return {'error': 'Correo o contraseña inválidos'}, 401
        
        # Generar tokens
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={
                'rol': user.rol,
                'email': user.correo,
                'nombre': user.nombre
            }
        )
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200
    

    def request_password_reset(self, email):
        """Solicita reseteo de contraseña"""
        user = self.user_repo.find_by_email(email)
        
        # Por seguridad, siempre devolvemos el mismo mensaje
        if user:
            # TODO: Enviar notificación al administrador
            pass
        
        return {
            'message': 'Si el correo está registrado, se ha enviado una solicitud al administrador'
        }, 200
    
    def change_password(self, user_id, old_password, new_password):
        """Cambia la contraseña de un usuario"""
        user = self.user_repo.find_by_id(user_id)
        
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        
        if not user.check_password(old_password):
            return {'error': 'Contraseña actual incorrecta'}, 400
        
    

        user.set_password(new_password)
        self.user_repo.update(user_id, {'contrasena': user.contrasena})
        #UserRepository.update(user_id, {'contraseña': user.contraseña})
        
        return {'message': 'Contraseña actualizada exitosamente'}, 200

    def create_user(self, data):
        # Este método es útil para el registro inicial o admin
        # Instanciamos un usuario temporal para usar su método set_password
        # Ojo: Esto es un truco para no importar bcrypt aquí
        from app.models.user import User
        temp_user = User()
        temp_user.set_password(data['contrasena'])
        data['contrasena'] = temp_user.contrasena
        
        return self.user_repo.create(**data)