# backend/app/services/auth_service.py
from flask_jwt_extended import create_access_token, create_refresh_token
from app.repositories import UserRepository

class AuthService:
    @staticmethod
    def login(email, password):
        """Autentica un usuario y genera tokens JWT"""
        user = UserRepository.find_by_email(email)
        
        if not user:
            return {'error': 'Correo o contraseña inválidos'}, 401
        
        if not user.activo:
            return {'error': 'Usuario inactivo'}, 403
        
        if not user.check_password(password):
            return {'error': 'Correo o contraseña inválidos'}, 401
        
        # Generar tokens
        access_token = create_access_token(identity=user.id, additional_claims={
            'rol': user.rol,
            'email': user.correo
        })
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def request_password_reset(email):
        """Solicita reseteo de contraseña"""
        user = UserRepository.find_by_email(email)
        
        # Por seguridad, siempre devolvemos el mismo mensaje
        if user:
            # TODO: Enviar notificación al administrador
            pass
        
        return {
            'message': 'Si el correo está registrado, se ha enviado una solicitud al administrador'
        }, 200
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Cambia la contraseña de un usuario"""
        user = UserRepository.find_by_id(user_id)
        
        if not user:
            return {'error': 'Usuario no encontrado'}, 404
        
        if not user.check_password(old_password):
            return {'error': 'Contraseña actual incorrecta'}, 400
        
        user.set_password(new_password)
        UserRepository.update(user_id, {'contraseña': user.contraseña})
        
        return {'message': 'Contraseña actualizada exitosamente'}, 200

