# backend/app/repositories/user_repository.py
from app.extensions import db
from app.models import User

class UserRepository:
    @staticmethod
    def create(user_data):
        """Crea un nuevo usuario"""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def find_by_id(user_id):
        """Busca usuario por ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def find_by_email(email):
        """Busca usuario por correo"""
        return User.query.filter_by(correo=email).first()
    
    @staticmethod
    def find_all(include_inactive=False):
        """Obtiene todos los usuarios"""
        query = User.query
        if not include_inactive:
            query = query.filter_by(activo=True)
        return query.all()
    
    @staticmethod
    def update(user_id, user_data):
        """Actualiza un usuario"""
        user = User.query.get(user_id)
        if user:
            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id, soft_delete=True):
        """Elimina un usuario (lógico o físico)"""
        user = User.query.get(user_id)
        if user:
            if soft_delete:
                user.activo = False
                db.session.commit()
            else:
                db.session.delete(user)
                db.session.commit()
        return user
    
    @staticmethod
    def find_by_role(role):
        """Busca usuarios por rol"""
        return User.query.filter_by(rol=role, activo=True).all()
