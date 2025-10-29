# backend/app/services/mqtt_service.py
import paho.mqtt.client as mqtt
import json
from threading import Thread
from flask import current_app
from app.services.measurement_service import MeasurementService

class MQTTService:
    def __init__(self, app=None):
        self.client = None
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Inicializa el servicio MQTT"""
        self.app = app
        
        # Configurar cliente MQTT
        self.client = mqtt.Client()
        
        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        # Credenciales si son necesarias
        if app.config.get('MQTT_USERNAME'):
            self.client.username_pw_set(
                app.config['MQTT_USERNAME'],
                app.config['MQTT_PASSWORD']
            )
        
        # Conectar en un thread separado
        thread = Thread(target=self._connect_mqtt)
        thread.daemon = True
        thread.start()
    
    def _connect_mqtt(self):
        """Conecta al broker MQTT"""
        try:
            self.client.connect(
                self.app.config['MQTT_BROKER_URL'],
                self.app.config['MQTT_BROKER_PORT'],
                60
            )
            self.client.loop_forever()
        except Exception as e:
            print(f"Error conectando a MQTT: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback cuando se conecta al broker"""
        if rc == 0:
            print("Conectado al broker MQTT")
            # Suscribirse al tópico
            topic = self.app.config.get('MQTT_TOPIC', 'environmental/measurements')
            client.subscribe(topic)
            print(f"Suscrito a: {topic}")
        else:
            print(f"Falló conexión MQTT con código: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback cuando llega un mensaje"""
        try:
            # Decodificar payload
            payload = json.loads(msg.payload.decode())
            print(f"Mensaje recibido: {payload}")
            
            # Estructura esperada:
            # {
            #   "nodo_id": 1,
            #   "temperatura": 25.5,
            #   "humedad": 60.0,
            #   "co2": 450.0
            # }
            
            # Guardar medición en contexto de aplicación
            with self.app.app_context():
                MeasurementService.save_measurement(payload)
                
        except json.JSONDecodeError:
            print(f"Error decodificando JSON: {msg.payload}")
        except Exception as e:
            print(f"Error procesando mensaje: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback cuando se desconecta"""
        if rc != 0:
            print(f"Desconexión inesperada. Código: {rc}")
    
    def publish(self, topic, payload):
        """Publica un mensaje"""
        if self.client:
            self.client.publish(topic, json.dumps(payload))

