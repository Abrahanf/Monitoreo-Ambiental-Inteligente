# backend/app/models/alert.py
from datetime import datetime
from app.extensions import db

class Alert(db.Model):
    __tablename__ = 'alertas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    hora = db.Column(db.Time, nullable=False)
    tipo = db.Column(db.Enum('Temperatura', 'Humedad', 'CO2'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    umbral = db.Column(db.Float, nullable=False)
    severidad = db.Column(db.Enum('Baja', 'Media', 'Alta', 'Crítica'), nullable=False)
    estado = db.Column(db.Enum('Activa', 'Resuelta', 'Pendiente'), default='Activa', nullable=False)
    mensaje = db.Column(db.Text, nullable=True) # no está en el MER
    
    # relaciones
    nodo_id = db.Column(db.Integer, db.ForeignKey('nodos.id'), nullable=False, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nodo_id': self.nodo_id,
            'fecha': self.fecha.isoformat(),
            'hora': self.hora.isoformat(),
            'tipo': self.tipo,
            'valor': self.valor,
            'umbral': self.umbral,
            'severidad': self.severidad,
            'estado': self.estado,
            'mensaje': self.mensaje,
        }

