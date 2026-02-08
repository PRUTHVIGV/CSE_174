import tensorflow as tf
import numpy as np
import json
import socket
import threading
import time
from datetime import datetime
import pickle
import hashlib

class FederatedServer:
    def __init__(self, port=8080, min_clients=3, rounds=10):
        self.port = port
        self.min_clients = min_clients
        self.rounds = rounds
        self.clients = {}
        self.global_model = None
        self.current_round = 0
        self.client_updates = {}
        self.model_history = []
        
    def initialize_global_model(self):
        """Initialize global model architecture"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.global_model = model
        return model
    
    def start_server(self):
        """Start federated learning server"""
        self.initialize_global_model()
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(10)
        
        print(f"🌐 Federated Learning Server started on port {self.port}")
        print(f"Waiting for {self.min_clients} clients...")
        
        while True:
            client_socket, address = server_socket.accept()
            client_id = f"client_{len(self.clients)}"
            self.clients[client_id] = {
                'socket': client_socket,
                'address': address,
                'last_seen': datetime.now()
            }
            
            print(f"Client {client_id} connected from {address}")
            
            # Start client handler thread
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_id, client_socket)
            )
            client_thread.start()
            
            # Start federated learning when enough clients
            if len(self.clients) >= self.min_clients and self.current_round == 0:
                fl_thread = threading.Thread(target=self.run_federated_learning)
                fl_thread.start()
    
    def handle_client(self, client_id, client_socket):
        """Handle individual client communication"""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                self.process_client_message(client_id, message)
                
        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
            client_socket.close()
    
    def process_client_message(self, client_id, message):
        """Process messages from clients"""
        if message['type'] == 'model_update':
            self.client_updates[client_id] = {
                'weights': message['weights'],
                'samples': message['samples'],
                'accuracy': message['accuracy'],
                'round': message['round']
            }
            print(f"Received update from {client_id} - Accuracy: {message['accuracy']:.4f}")
        
        elif message['type'] == 'ready':
            print(f"Client {client_id} is ready for training")
    
    def run_federated_learning(self):
        """Run federated learning rounds"""
        for round_num in range(self.rounds):
            self.current_round = round_num + 1
            print(f"\n🔄 Starting Federated Learning Round {self.current_round}")
            
            # Send global model to all clients
            self.broadcast_global_model()
            
            # Wait for client updates
            self.wait_for_client_updates()
            
            # Aggregate updates
            self.aggregate_updates()
            
            # Evaluate global model
            self.evaluate_global_model()
            
            time.sleep(2)  # Brief pause between rounds
        
        print("🎉 Federated Learning completed!")
        self.save_final_model()
    
    def broadcast_global_model(self):
        """Send global model to all clients"""
        global_weights = self.global_model.get_weights()
        
        message = {
            'type': 'global_model',
            'weights': global_weights,
            'round': self.current_round
        }
        
        for client_id, client_info in self.clients.items():
            try:
                client_info['socket'].send(pickle.dumps(message))
                print(f"Sent global model to {client_id}")
            except Exception as e:
                print(f"Failed to send model to {client_id}: {e}")
    
    def wait_for_client_updates(self):
        """Wait for all clients to send updates"""
        print("⏳ Waiting for client updates...")
        
        timeout = 60  # 60 seconds timeout
        start_time = time.time()
        
        while len(self.client_updates) < len(self.clients):
            if time.time() - start_time > timeout:
                print("⚠️ Timeout waiting for client updates")
                break
            time.sleep(1)
        
        print(f"Received {len(self.client_updates)} client updates")
    
    def aggregate_updates(self):
        """Aggregate client model updates using FedAvg"""
        if not self.client_updates:
            return
        
        # Calculate total samples
        total_samples = sum(update['samples'] for update in self.client_updates.values())
        
        # Initialize aggregated weights
        aggregated_weights = None
        
        for client_id, update in self.client_updates.items():
            client_weights = update['weights']
            client_samples = update['samples']
            weight_factor = client_samples / total_samples
            
            if aggregated_weights is None:
                aggregated_weights = [w * weight_factor for w in client_weights]
            else:
                for i, w in enumerate(client_weights):
                    aggregated_weights[i] += w * weight_factor
        
        # Update global model
        self.global_model.set_weights(aggregated_weights)
        
        # Store model history
        avg_accuracy = np.mean([update['accuracy'] for update in self.client_updates.values()])
        self.model_history.append({
            'round': self.current_round,
            'avg_client_accuracy': avg_accuracy,
            'num_clients': len(self.client_updates),
            'total_samples': total_samples
        })
        
        print(f"✅ Aggregated updates from {len(self.client_updates)} clients")
        print(f"Average client accuracy: {avg_accuracy:.4f}")
        
        # Clear updates for next round
        self.client_updates = {}
    
    def evaluate_global_model(self):
        """Evaluate global model performance"""
        # This would typically use a validation dataset
        print(f"Global model updated for round {self.current_round}")
    
    def save_final_model(self):
        """Save the final federated model"""
        self.global_model.save('federated_cattle_model.h5')
        
        # Save training history
        with open('federated_history.json', 'w') as f:
            json.dump(self.model_history, f, indent=2)
        
        print("💾 Final federated model saved!")

class FederatedClient:
    def __init__(self, client_id, server_host='localhost', server_port=8080):
        self.client_id = client_id
        self.server_host = server_host
        self.server_port = server_port
        self.local_model = None
        self.local_data = None
        self.socket = None
        
    def connect_to_server(self):
        """Connect to federated learning server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_host, self.server_port))
        
        # Send ready message
        ready_message = {'type': 'ready', 'client_id': self.client_id}
        self.socket.send(pickle.dumps(ready_message))
        
        print(f"🔗 Client {self.client_id} connected to server")
    
    def load_local_data(self, X_train, y_train):
        """Load local training data"""
        self.local_data = (X_train, y_train)
        print(f"📊 Loaded {len(X_train)} local samples")
    
    def simulate_local_data(self, num_samples=1000):
        """Simulate local data for testing"""
        X_train = np.random.random((num_samples, 224, 224, 3))
        y_train = np.random.randint(0, 10, num_samples)
        self.load_local_data(X_train, y_train)
    
    def start_training(self):
        """Start federated training process"""
        try:
            while True:
                # Receive message from server
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = pickle.loads(data)
                
                if message['type'] == 'global_model':
                    self.update_local_model(message['weights'])
                    self.train_local_model()
                    self.send_model_update(message['round'])
                
        except Exception as e:
            print(f"Training error: {e}")
        finally:
            self.socket.close()
    
    def update_local_model(self, global_weights):
        """Update local model with global weights"""
        if self.local_model is None:
            self.initialize_local_model()
        
        self.local_model.set_weights(global_weights)
        print(f"📥 Updated local model with global weights")
    
    def initialize_local_model(self):
        """Initialize local model architecture"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.local_model = model
    
    def train_local_model(self):
        """Train local model on local data"""
        if self.local_data is None:
            print("⚠️ No local data available")
            return
        
        X_train, y_train = self.local_data
        
        print(f"🏋️ Training local model on {len(X_train)} samples...")
        
        history = self.local_model.fit(
            X_train, y_train,
            epochs=5,
            batch_size=32,
            verbose=0
        )
        
        self.local_accuracy = history.history['accuracy'][-1]
        print(f"Local training accuracy: {self.local_accuracy:.4f}")
    
    def send_model_update(self, round_num):
        """Send model update to server"""
        local_weights = self.local_model.get_weights()
        
        update_message = {
            'type': 'model_update',
            'weights': local_weights,
            'samples': len(self.local_data[0]) if self.local_data else 0,
            'accuracy': self.local_accuracy,
            'round': round_num,
            'client_id': self.client_id
        }
        
        self.socket.send(pickle.dumps(update_message))
        print(f"📤 Sent model update to server")

class PrivacyPreservingFL:
    def __init__(self):
        self.noise_multiplier = 1.0
        self.l2_norm_clip = 1.0
    
    def add_differential_privacy(self, gradients):
        """Add differential privacy noise to gradients"""
        noisy_gradients = []
        
        for grad in gradients:
            # Clip gradients
            clipped_grad = tf.clip_by_norm(grad, self.l2_norm_clip)
            
            # Add Gaussian noise
            noise = tf.random.normal(
                shape=tf.shape(clipped_grad),
                stddev=self.noise_multiplier * self.l2_norm_clip
            )
            
            noisy_grad = clipped_grad + noise
            noisy_gradients.append(noisy_grad)
        
        return noisy_gradients
    
    def secure_aggregation(self, client_updates):
        """Implement secure aggregation protocol"""
        # Simplified secure aggregation
        encrypted_updates = []
        
        for update in client_updates:
            # Add random mask (simplified)
            mask = np.random.random(np.array(update).shape)
            encrypted_update = np.array(update) + mask
            encrypted_updates.append(encrypted_update)
        
        return encrypted_updates

def run_federated_simulation():
    """Run federated learning simulation"""
    print("🚀 Starting Federated Learning Simulation")
    
    # Start server in separate thread
    server = FederatedServer(min_clients=3, rounds=5)
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(2)  # Wait for server to start
    
    # Create and start clients
    clients = []
    for i in range(3):
        client = FederatedClient(f"client_{i}")
        client.simulate_local_data(num_samples=500)
        clients.append(client)
        
        # Connect and start training in separate thread
        client.connect_to_server()
        client_thread = threading.Thread(target=client.start_training)
        client_thread.daemon = True
        client_thread.start()
    
    # Keep simulation running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping federated learning simulation")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['server', 'client', 'simulate'], default='simulate')
    parser.add_argument('--client-id', default='client_0')
    parser.add_argument('--port', type=int, default=8080)
    
    args = parser.parse_args()
    
    if args.mode == 'server':
        server = FederatedServer(port=args.port)
        server.start_server()
    
    elif args.mode == 'client':
        client = FederatedClient(args.client_id)
        client.simulate_local_data()
        client.connect_to_server()
        client.start_training()
    
    else:
        run_federated_simulation()