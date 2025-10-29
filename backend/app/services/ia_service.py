# backend/app/services/ia_service.py
import requests
from flask import current_app

class IAService:
    @staticmethod
    def analyze_measurement(measurement_data):
        """Envía medición al microservicio de IA para análisis"""
        try:
            url = f"{current_app.config['IA_SERVICE_URL']}/api/analyze"
            response = requests.post(url, json=measurement_data, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Error en servicio IA', 'status': response.status_code}
                
        except requests.exceptions.RequestException as e:
            print(f"Error conectando con servicio IA: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def train_model(dataset_path, parameters):
        """Solicita entrenamiento de un nuevo modelo"""
        try:
            url = f"{current_app.config['IA_SERVICE_URL']}/api/train"
            data = {
                'dataset_path': dataset_path,
                'parameters': parameters
            }
            response = requests.post(url, json=data, timeout=300)  # 5 minutos timeout
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Error entrenando modelo', 'status': response.status_code}
                
        except requests.exceptions.RequestException as e:
            print(f"Error en entrenamiento: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def get_model_info():
        """Obtiene información del modelo actual"""
        try:
            url = f"{current_app.config['IA_SERVICE_URL']}/api/model/info"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Error obteniendo info del modelo'}
                
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo info: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def update_sensitivity(sensitivity):
        """Actualiza la sensibilidad del modelo"""
        try:
            url = f"{current_app.config['IA_SERVICE_URL']}/api/model/sensitivity"
            response = requests.put(url, json={'sensitivity': sensitivity}, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Error actualizando sensibilidad'}
                
        except requests.exceptions.RequestException as e:
            print(f"Error actualizando sensibilidad: {e}")
            return {'error': str(e)}
