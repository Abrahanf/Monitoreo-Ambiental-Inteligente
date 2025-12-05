from app.models.sensor import Sensor
from app.extensions import db

class SensorRepository:
    
    def get_by_node(self, nodo_id):
        """Obtiene todos los sensores de un nodo"""
        return Sensor.query.filter_by(nodo_id=nodo_id).all()

    def create(self, **kwargs):
        """
        ESTA ES LA FUNCIÓN QUE 'AGREGA' EL SENSOR.
        Se llama 'create' por convención CRUD, pero es tu 'add_sensor'.
        """
        sensor = Sensor(**kwargs)
        db.session.add(sensor)
        db.session.commit()
        return sensor

    def update(self, sensor_id, data):
        """Actualiza un sensor existente"""
        sensor = Sensor.query.get(sensor_id)
        if sensor:
            for key, value in data.items():
                if hasattr(sensor, key):
                    setattr(sensor, key, value)
            db.session.commit()
        return sensor

    def delete(self, sensor_id):
        """Elimina un sensor por ID"""
        sensor = Sensor.query.get(sensor_id)
        if sensor:
            db.session.delete(sensor)
            db.session.commit()
        return sensor