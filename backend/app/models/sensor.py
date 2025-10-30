# backend/app/models/sensor.py
from app.extensions import db

class Sensor(db.Model):
    __tablename__ = 'sensores'
    
    id = db.Column(db.Integer, primary_key=True)
    nodo_id = db.Column(db.Integer, db.ForeignKey('nodos.id'), nullable=False)
    sensor = db.Column(db.String(50), nullable=False)  # DHT22, MQ-135
    variable = db.Column(db.String(50), nullable=False)  # temp, hum, CO2
    umbral_min = db.Column(db.Float, nullable=False)
    umbral_max = db.Column(db.Float, nullable=False)
    velocidad_muestreo = db.Column(db.Integer, default=5)  # segundos
    estado = db.Column(db.Enum('ON', 'OFF'), default='ON', nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nodo_id': self.nodo_id,
            'sensor': self.sensor,
            'variable': self.variable,
            'umbral_min': self.umbral_min,
            'umbral_max': self.umbral_max,
            'velocidad_muestreo': self.velocidad_muestreo,
            'estado': self.estado
        }

