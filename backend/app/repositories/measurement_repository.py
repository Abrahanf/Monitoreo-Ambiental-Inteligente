# backend/app/repositories/measurement_repository.py
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from app.extensions import db
from app.models import Measurement

class MeasurementRepository:
    @staticmethod
    def create(measurement_data):
        """Crea una nueva medición"""
        measurement = Measurement(**measurement_data)
        db.session.add(measurement)
        db.session.commit()
        return measurement
    
    @staticmethod
    def create_bulk(measurements_data):
        """Crea múltiples mediciones de forma eficiente"""
        measurements = [Measurement(**data) for data in measurements_data]
        db.session.bulk_save_objects(measurements)
        db.session.commit()
        return measurements
    
    @staticmethod
    def find_by_node(node_id, start_date=None, end_date=None, limit=1000):
        """Obtiene mediciones de un nodo en un rango de fechas"""
        query = Measurement.query.filter_by(nodo_id=node_id)
        
        if start_date:
            query = query.filter(Measurement.fecha_hora >= start_date)
        if end_date:
            query = query.filter(Measurement.fecha_hora <= end_date)
        
        return query.order_by(Measurement.fecha_hora.desc()).limit(limit).all()
    
    @staticmethod
    def find_latest_by_node(node_id, limit=1):
        """Obtiene las últimas mediciones de un nodo"""
        return Measurement.query.filter_by(nodo_id=node_id)\
            .order_by(Measurement.fecha_hora.desc())\
            .limit(limit).all()
    
    @staticmethod
    def get_statistics(node_id, start_date, end_date):
        """Obtiene estadísticas de un nodo en un período"""
        stats = db.session.query(
            func.avg(Measurement.temperatura).label('temp_avg'),
            func.min(Measurement.temperatura).label('temp_min'),
            func.max(Measurement.temperatura).label('temp_max'),
            func.avg(Measurement.humedad).label('hum_avg'),
            func.min(Measurement.humedad).label('hum_min'),
            func.max(Measurement.humedad).label('hum_max'),
            func.avg(Measurement.co2).label('co2_avg'),
            func.min(Measurement.co2).label('co2_min'),
            func.max(Measurement.co2).label('co2_max'),
            func.count(Measurement.id).label('count')
        ).filter(
            and_(
                Measurement.nodo_id == node_id,
                Measurement.fecha_hora >= start_date,
                Measurement.fecha_hora <= end_date
            )
        ).first()
        
        return {
            'temperatura': {
                'promedio': float(stats.temp_avg) if stats.temp_avg else 0,
                'minimo': float(stats.temp_min) if stats.temp_min else 0,
                'maximo': float(stats.temp_max) if stats.temp_max else 0
            },
            'humedad': {
                'promedio': float(stats.hum_avg) if stats.hum_avg else 0,
                'minimo': float(stats.hum_min) if stats.hum_min else 0,
                'maximo': float(stats.hum_max) if stats.hum_max else 0
            },
            'co2': {
                'promedio': float(stats.co2_avg) if stats.co2_avg else 0,
                'minimo': float(stats.co2_min) if stats.co2_min else 0,
                'maximo': float(stats.co2_max) if stats.co2_max else 0
            },
            'total_mediciones': stats.count
        }
    
    @staticmethod
    def get_hourly_averages(node_id, start_date, end_date):
        """Obtiene promedios por hora"""
        results = db.session.query(
            func.date_format(Measurement.fecha_hora, '%Y-%m-%d %H:00:00').label('hora'),
            func.avg(Measurement.temperatura).label('temp'),
            func.avg(Measurement.humedad).label('hum'),
            func.avg(Measurement.co2).label('co2')
        ).filter(
            and_(
                Measurement.nodo_id == node_id,
                Measurement.fecha_hora >= start_date,
                Measurement.fecha_hora <= end_date
            )
        ).group_by('hora').all()
        
        return [{
            'fecha_hora': r.hora,
            'temperatura': float(r.temp),
            'humedad': float(r.hum),
            'co2': float(r.co2)
        } for r in results]
    
    @staticmethod
    def delete_old_measurements(days=90):
        """Elimina mediciones antiguas (limpieza automática)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = Measurement.query.filter(
            Measurement.fecha_hora < cutoff_date
        ).delete()
        db.session.commit()
        return deleted
