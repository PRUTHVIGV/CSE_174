import json
import time
import requests
import cv2
import numpy as np
from datetime import datetime
import sqlite3
import paho.mqtt.client as mqtt
from threading import Thread
import schedule

class IoTCattleMonitor:
    def __init__(self, model_path, mqtt_broker="localhost", mqtt_port=1883):
        self.model = tf.keras.models.load_model(model_path)
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.setup_database()
        self.setup_mqtt()
        
        self.breeds = [
            'Gir', 'Sahiwal', 'Red_Sindhi', 'Tharparkar', 'Ongole',
            'Hariana', 'Kankrej', 'Rathi', 'Murrah_Buffalo', 'Mehsana_Buffalo'
        ]
    
    def setup_database(self):
        """Setup SQLite database for cattle records"""
        self.conn = sqlite3.connect('cattle_monitoring.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cattle_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cattle_id TEXT,
                breed TEXT,
                confidence REAL,
                location TEXT,
                temperature REAL,
                humidity REAL,
                activity_level TEXT,
                health_status TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cattle_id TEXT,
                alert_type TEXT,
                message TEXT,
                severity TEXT
            )
        ''')
        
        self.conn.commit()
    
    def setup_mqtt(self):
        """Setup MQTT client for IoT communication"""
        def on_connect(client, userdata, flags, rc):
            print(f"Connected to MQTT broker with result code {rc}")
            client.subscribe("cattle/sensor/+")
            client.subscribe("cattle/camera/+")
        
        def on_message(client, userdata, msg):
            self.process_iot_message(msg.topic, msg.payload.decode())
        
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.mqtt_client.loop_start()
    
    def process_iot_message(self, topic, payload):
        """Process incoming IoT messages"""
        try:
            data = json.loads(payload)
            
            if "sensor" in topic:
                self.process_sensor_data(data)
            elif "camera" in topic:
                self.process_camera_data(data)
                
        except Exception as e:
            print(f"Error processing IoT message: {e}")
    
    def process_sensor_data(self, data):
        """Process sensor data (temperature, humidity, GPS, etc.)"""
        cattle_id = data.get('cattle_id')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        gps_location = data.get('location')
        activity = data.get('activity_level', 'normal')
        
        # Health monitoring based on sensor data
        health_status = self.assess_health(temperature, humidity, activity)
        
        # Store in database
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO cattle_records 
            (timestamp, cattle_id, temperature, humidity, location, activity_level, health_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), cattle_id, temperature, humidity, 
              json.dumps(gps_location), activity, health_status))
        
        self.conn.commit()
        
        # Generate alerts if needed
        if health_status != 'healthy':
            self.generate_alert(cattle_id, 'health', f'Health concern detected: {health_status}', 'medium')
    
    def process_camera_data(self, data):
        """Process camera data for breed recognition"""
        cattle_id = data.get('cattle_id')
        image_path = data.get('image_path')
        
        if image_path:
            breed, confidence = self.predict_breed(image_path)
            
            # Update database
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE cattle_records 
                SET breed = ?, confidence = ?
                WHERE cattle_id = ? AND timestamp = (
                    SELECT MAX(timestamp) FROM cattle_records WHERE cattle_id = ?
                )
            ''', (breed, confidence, cattle_id, cattle_id))
            
            self.conn.commit()
            
            # Publish result
            result = {
                'cattle_id': cattle_id,
                'breed': breed,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat()
            }
            
            self.mqtt_client.publish(f"cattle/recognition/{cattle_id}", json.dumps(result))
    
    def predict_breed(self, image_path):
        """Predict cattle breed from image"""
        img = cv2.imread(image_path)
        img = cv2.resize(img, (224, 224))
        img = np.expand_dims(img, axis=0) / 255.0
        
        predictions = self.model.predict(img)
        pred_class = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        return self.breeds[pred_class], confidence
    
    def assess_health(self, temperature, humidity, activity):
        """Assess cattle health based on sensor data"""
        if temperature > 39.5:  # High fever
            return 'fever'
        elif temperature < 37.5:  # Low temperature
            return 'hypothermia'
        elif activity == 'low' and temperature > 39:
            return 'sick'
        elif humidity > 80 and temperature > 38:
            return 'heat_stress'
        else:
            return 'healthy'
    
    def generate_alert(self, cattle_id, alert_type, message, severity):
        """Generate and store alerts"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, cattle_id, alert_type, message, severity)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), cattle_id, alert_type, message, severity))
        
        self.conn.commit()
        
        # Publish alert
        alert = {
            'cattle_id': cattle_id,
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat()
        }
        
        self.mqtt_client.publish("cattle/alerts", json.dumps(alert))
        print(f"🚨 ALERT: {message}")
    
    def get_cattle_status(self, cattle_id):
        """Get current status of a specific cattle"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM cattle_records 
            WHERE cattle_id = ? 
            ORDER BY timestamp DESC LIMIT 1
        ''', (cattle_id,))
        
        record = cursor.fetchone()
        if record:
            return {
                'cattle_id': cattle_id,
                'last_seen': record[1],
                'breed': record[3],
                'confidence': record[4],
                'location': json.loads(record[5]) if record[5] else None,
                'temperature': record[6],
                'humidity': record[7],
                'activity': record[8],
                'health': record[9]
            }
        return None
    
    def generate_daily_report(self):
        """Generate daily monitoring report"""
        cursor = self.conn.cursor()
        
        # Get today's data
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT cattle_id, breed, AVG(temperature), AVG(humidity), health_status, COUNT(*)
            FROM cattle_records 
            WHERE DATE(timestamp) = ?
            GROUP BY cattle_id
        ''', (today,))
        
        records = cursor.fetchall()
        
        report = {
            'date': today,
            'total_cattle': len(records),
            'cattle_data': []
        }
        
        for record in records:
            cattle_data = {
                'id': record[0],
                'breed': record[1],
                'avg_temperature': round(record[2], 2) if record[2] else None,
                'avg_humidity': round(record[3], 2) if record[3] else None,
                'health_status': record[4],
                'readings_count': record[5]
            }
            report['cattle_data'].append(cattle_data)
        
        # Get alerts
        cursor.execute('''
            SELECT alert_type, COUNT(*) 
            FROM alerts 
            WHERE DATE(timestamp) = ?
            GROUP BY alert_type
        ''', (today,))
        
        alerts = cursor.fetchall()
        report['alerts_summary'] = {alert[0]: alert[1] for alert in alerts}
        
        return report

class EdgeAIProcessor:
    def __init__(self, model_path):
        self.model = tf.lite.Interpreter(model_path=model_path)
        self.model.allocate_tensors()
        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()
    
    def process_edge_inference(self, image_data):
        """Process inference on edge device"""
        # Preprocess
        img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (224, 224))
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        
        # Inference
        self.model.set_tensor(self.input_details[0]['index'], img)
        self.model.invoke()
        output = self.model.get_tensor(self.output_details[0]['index'])
        
        return output[0]

class SmartFarmDashboard:
    def __init__(self, monitor):
        self.monitor = monitor
    
    def create_dashboard(self):
        """Create web dashboard for farm monitoring"""
        from flask import Flask, render_template, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def dashboard():
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Smart Cattle Farm Dashboard</title>
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                <style>
                    body { font-family: Arial; margin: 20px; background: #f0f0f0; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .card { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                    .alert { background: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px 0; }
                    .healthy { color: #4caf50; }
                    .warning { color: #ff9800; }
                    .critical { color: #f44336; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐄 Smart Cattle Farm Dashboard</h1>
                    
                    <div class="card">
                        <h2>Farm Overview</h2>
                        <div id="overview"></div>
                    </div>
                    
                    <div class="status-grid">
                        <div class="card">
                            <h3>Cattle Status</h3>
                            <div id="cattle-status"></div>
                        </div>
                        
                        <div class="card">
                            <h3>Recent Alerts</h3>
                            <div id="alerts"></div>
                        </div>
                        
                        <div class="card">
                            <h3>Environmental Data</h3>
                            <div id="environmental"></div>
                        </div>
                    </div>
                </div>
                
                <script>
                    function updateDashboard() {
                        fetch('/api/status')
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('overview').innerHTML = 
                                    `<p>Total Cattle: ${data.total_cattle}</p>
                                     <p>Healthy: <span class="healthy">${data.healthy_count}</span></p>
                                     <p>Alerts: <span class="warning">${data.alert_count}</span></p>`;
                            });
                    }
                    
                    setInterval(updateDashboard, 5000);
                    updateDashboard();
                </script>
            </body>
            </html>
            '''
        
        @app.route('/api/status')
        def api_status():
            cursor = self.monitor.conn.cursor()
            
            # Get cattle count
            cursor.execute('SELECT COUNT(DISTINCT cattle_id) FROM cattle_records')
            total_cattle = cursor.fetchone()[0]
            
            # Get healthy count
            cursor.execute('''
                SELECT COUNT(DISTINCT cattle_id) FROM cattle_records 
                WHERE health_status = "healthy" AND DATE(timestamp) = DATE("now")
            ''')
            healthy_count = cursor.fetchone()[0]
            
            # Get alert count
            cursor.execute('SELECT COUNT(*) FROM alerts WHERE DATE(timestamp) = DATE("now")')
            alert_count = cursor.fetchone()[0]
            
            return jsonify({
                'total_cattle': total_cattle,
                'healthy_count': healthy_count,
                'alert_count': alert_count
            })
        
        return app

def simulate_iot_data():
    """Simulate IoT sensor data for testing"""
    import random
    
    cattle_ids = ['COW001', 'COW002', 'COW003', 'BUF001', 'BUF002']
    
    while True:
        for cattle_id in cattle_ids:
            # Simulate sensor data
            sensor_data = {
                'cattle_id': cattle_id,
                'temperature': round(random.uniform(37.0, 40.0), 1),
                'humidity': round(random.uniform(40, 90), 1),
                'location': {
                    'lat': round(random.uniform(20.0, 30.0), 6),
                    'lon': round(random.uniform(70.0, 80.0), 6)
                },
                'activity_level': random.choice(['low', 'normal', 'high'])
            }
            
            # Publish to MQTT
            client = mqtt.Client()
            client.connect("localhost", 1883, 60)
            client.publish(f"cattle/sensor/{cattle_id}", json.dumps(sensor_data))
            client.disconnect()
        
        time.sleep(30)  # Send data every 30 seconds

if __name__ == "__main__":
    # Initialize IoT monitoring system
    monitor = IoTCattleMonitor('cattle_breed_model.h5')
    
    # Create dashboard
    dashboard = SmartFarmDashboard(monitor)
    app = dashboard.create_dashboard()
    
    # Schedule daily reports
    schedule.every().day.at("08:00").do(lambda: print(monitor.generate_daily_report()))
    
    print("🌐 IoT Cattle Monitoring System Started!")
    print("Dashboard: http://localhost:5000")
    
    # Start dashboard
    app.run(host='0.0.0.0', port=5000, debug=True)