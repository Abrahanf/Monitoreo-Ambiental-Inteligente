# backend/app/models/node.py
from datetime import datetime
from app.extensions import db

class Node(db.Model):
    __tablename__ = 'nodos'
    
    id = db.Column(db.Integer, primary_key=True)
    ubicacion = db.Column(db.String(200), nullable=False)
    microcontrolador = db.Column(db.String(50), nullable=False, default='ESP32')
    velocidad_datos = db.Column(db.Integer, nullable=False, default=60)  # segundos
    estado = db.Column(db.Enum('ON', 'OFF'), default='ON', nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_conexion = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    sensores = db.relationship('Sensor', backref='nodo', lazy='dynamic', cascade='all, delete-orphan')
    mediciones = db.relationship('Measurement', backref='nodo', lazy='dynamic', cascade='all, delete-orphan')
    alertas = db.relationship('Alert', backref='nodo', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ubicacion': self.ubicacion,
            'microcontrolador': self.microcontrolador,
            'velocidad_datos': self.velocidad_datos,
            'estado': self.estado,
            'fecha_registro': self.fecha_registro.isoformat(),
            'ultima_conexion': self.ultima_conexion.isoformat() if self.ultima_conexion else None,
            'sensores': [s.to_dict() for s in self.sensores.all()]
        }

