# backend/app/mqtt_worker/listener.py
import paho.mqtt.client as mqtt
import json
import os
from app import create_app
from app.services.monitoring_service import MonitoringService

# Inicializar la app de Flask para tener contexto de BD
app = create_app()

# Instanciar el servicio que creamos
# (Asegúrate que el archivo monitoring_service.py existe en services/)
monitoring_service = MonitoringService()

def on_connect(client, userdata, flags, rc):
    print("Worker conectado al Broker MQTT!")
    # Suscribirse a todo lo que envíen los nodos
    client.subscribe("environmental/measurements") 

def on_message(client, userdata, msg):
    try:
        with app.app_context():
            payload = json.loads(msg.payload.decode())
            print(f"Worker recibió: {payload}")
            
            # CAMBIO AQUÍ: Leemos 'nodo_id' del JSON
            monitoring_service.register_measurement(
                payload.get('nodo_id'), 
                payload.get('temp'),
                payload.get('hum'),
                payload.get('co2')
            )
            print("Dato procesado correctamente")
            
    except Exception as e:
        print(f"Error en worker: {e}")

if __name__ == '__main__':
    # Configuración básica
    broker_url = os.environ.get('MQTT_BROKER_URL', 'mqtt_broker')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"Iniciando conexión a {broker_url}...")
    client.connect(broker_url, 1883, 60)
    client.loop_forever()