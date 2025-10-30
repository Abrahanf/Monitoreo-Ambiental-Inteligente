# backend/app/models/user.py
from datetime import datetime
from app.extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False, index=True)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('usuario', 'administrador'), default='usuario', nullable=False)
    nodo_id = db.Column(db.Integer, db.ForeignKey('nodos.id'), nullable=True)
    ubicacion_asignada = db.Column(db.String(200), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    nodo = db.relationship('Node', backref='usuarios', foreign_keys=[nodo_id])
    reportes = db.relationship('Report', backref='usuario', lazy='dynamic')
    
    def set_password(self, password):
        """Hashea la contraseña"""
        self.contrasena = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return bcrypt.check_password_hash(self.contrasena, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'rol': self.rol,
            'nodo_id': self.nodo_id,
            'ubicacion_asignada': self.ubicacion_asignada,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'activo': self.activo
        }

