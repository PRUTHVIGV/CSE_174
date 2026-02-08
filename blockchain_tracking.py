import hashlib
import json
import time
from datetime import datetime
import sqlite3
from cryptography.fernet import Fernet
import qrcode
from PIL import Image
import io
import base64

class CattleBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.mining_reward = 10
        self.difficulty = 2
        self.create_genesis_block()
        self.setup_database()
    
    def setup_database(self):
        """Setup database for blockchain storage"""
        self.conn = sqlite3.connect('cattle_blockchain.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                block_hash TEXT UNIQUE,
                previous_hash TEXT,
                timestamp TEXT,
                data TEXT,
                nonce INTEGER,
                merkle_root TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cattle_registry (
                cattle_id TEXT PRIMARY KEY,
                breed TEXT,
                birth_date TEXT,
                owner_id TEXT,
                farm_location TEXT,
                parent_ids TEXT,
                health_records TEXT,
                ownership_history TEXT,
                certification_hash TEXT
            )
        ''')
        
        self.conn.commit()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(0, "0", {
            "type": "genesis",
            "message": "Cattle Blockchain Genesis Block",
            "timestamp": datetime.now().isoformat()
        })
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add transaction to pending pool"""
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mine pending transactions into a new block"""
        reward_transaction = Transaction(None, mining_reward_address, self.mining_reward, "mining_reward")
        self.pending_transactions.append(reward_transaction)
        
        block = Block(
            len(self.chain),
            self.get_latest_block().hash,
            self.pending_transactions
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        # Store in database
        self.store_block(block)
        
        self.pending_transactions = []
    
    def store_block(self, block):
        """Store block in database"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO blocks (block_hash, previous_hash, timestamp, data, nonce, merkle_root)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (block.hash, block.previous_hash, block.timestamp, 
              json.dumps(block.data), block.nonce, block.merkle_root))
        self.conn.commit()
    
    def register_cattle(self, cattle_data):
        """Register new cattle on blockchain"""
        transaction = Transaction(
            from_address="system",
            to_address=cattle_data['cattle_id'],
            amount=0,
            transaction_type="cattle_registration",
            data=cattle_data
        )
        
        self.add_transaction(transaction)
        
        # Store in registry
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO cattle_registry 
            (cattle_id, breed, birth_date, owner_id, farm_location, parent_ids, health_records, ownership_history, certification_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cattle_data['cattle_id'],
            cattle_data['breed'],
            cattle_data['birth_date'],
            cattle_data['owner_id'],
            cattle_data['farm_location'],
            json.dumps(cattle_data.get('parent_ids', [])),
            json.dumps(cattle_data.get('health_records', [])),
            json.dumps([cattle_data['owner_id']]),
            self.calculate_hash(json.dumps(cattle_data))
        ))
        self.conn.commit()
        
        return transaction
    
    def transfer_ownership(self, cattle_id, from_owner, to_owner, price=0):
        """Transfer cattle ownership"""
        transaction = Transaction(
            from_address=from_owner,
            to_address=to_owner,
            amount=price,
            transaction_type="ownership_transfer",
            data={
                'cattle_id': cattle_id,
                'transfer_date': datetime.now().isoformat(),
                'price': price
            }
        )
        
        self.add_transaction(transaction)
        
        # Update registry
        cursor = self.conn.cursor()
        cursor.execute('SELECT ownership_history FROM cattle_registry WHERE cattle_id = ?', (cattle_id,))
        result = cursor.fetchone()
        
        if result:
            history = json.loads(result[0])
            history.append({
                'owner': to_owner,
                'date': datetime.now().isoformat(),
                'price': price
            })
            
            cursor.execute('''
                UPDATE cattle_registry 
                SET owner_id = ?, ownership_history = ?
                WHERE cattle_id = ?
            ''', (to_owner, json.dumps(history), cattle_id))
            self.conn.commit()
        
        return transaction
    
    def add_health_record(self, cattle_id, health_data):
        """Add health record to cattle"""
        transaction = Transaction(
            from_address="veterinarian",
            to_address=cattle_id,
            amount=0,
            transaction_type="health_record",
            data=health_data
        )
        
        self.add_transaction(transaction)
        
        # Update registry
        cursor = self.conn.cursor()
        cursor.execute('SELECT health_records FROM cattle_registry WHERE cattle_id = ?', (cattle_id,))
        result = cursor.fetchone()
        
        if result:
            records = json.loads(result[0])
            records.append(health_data)
            
            cursor.execute('''
                UPDATE cattle_registry 
                SET health_records = ?
                WHERE cattle_id = ?
            ''', (json.dumps(records), cattle_id))
            self.conn.commit()
        
        return transaction
    
    def verify_cattle_authenticity(self, cattle_id):
        """Verify cattle authenticity using blockchain"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM cattle_registry WHERE cattle_id = ?', (cattle_id,))
        result = cursor.fetchone()
        
        if not result:
            return {"valid": False, "message": "Cattle not found in registry"}
        
        # Verify hash integrity
        cattle_data = {
            'cattle_id': result[0],
            'breed': result[1],
            'birth_date': result[2],
            'owner_id': result[3],
            'farm_location': result[4]
        }
        
        calculated_hash = self.calculate_hash(json.dumps(cattle_data))
        stored_hash = result[8]
        
        if calculated_hash == stored_hash:
            return {
                "valid": True,
                "cattle_data": cattle_data,
                "ownership_history": json.loads(result[7]),
                "health_records": json.loads(result[6])
            }
        else:
            return {"valid": False, "message": "Data integrity compromised"}
    
    def calculate_hash(self, data):
        """Calculate SHA-256 hash"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True

class Block:
    def __init__(self, index, previous_hash, data):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate block hash"""
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}{self.nonce}{self.merkle_root}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def calculate_merkle_root(self):
        """Calculate Merkle root of transactions"""
        if isinstance(self.data, list):
            hashes = [hashlib.sha256(json.dumps(tx.__dict__).encode()).hexdigest() for tx in self.data]
        else:
            hashes = [hashlib.sha256(json.dumps(self.data).encode()).hexdigest()]
        
        while len(hashes) > 1:
            new_hashes = []
            for i in range(0, len(hashes), 2):
                if i + 1 < len(hashes):
                    combined = hashes[i] + hashes[i + 1]
                else:
                    combined = hashes[i] + hashes[i]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            hashes = new_hashes
        
        return hashes[0] if hashes else ""
    
    def mine_block(self, difficulty):
        """Mine block with proof of work"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")

class Transaction:
    def __init__(self, from_address, to_address, amount, transaction_type, data=None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.transaction_type = transaction_type
        self.data = data or {}
        self.timestamp = datetime.now().isoformat()
        self.transaction_id = self.calculate_transaction_id()
    
    def calculate_transaction_id(self):
        """Calculate unique transaction ID"""
        tx_string = f"{self.from_address}{self.to_address}{self.amount}{self.timestamp}{json.dumps(self.data)}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

class CattleCertification:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def generate_certificate(self, cattle_id):
        """Generate digital certificate for cattle"""
        verification = self.blockchain.verify_cattle_authenticity(cattle_id)
        
        if not verification['valid']:
            return None
        
        certificate_data = {
            'cattle_id': cattle_id,
            'breed': verification['cattle_data']['breed'],
            'owner': verification['cattle_data']['owner_id'],
            'issue_date': datetime.now().isoformat(),
            'blockchain_hash': self.blockchain.calculate_hash(json.dumps(verification['cattle_data'])),
            'certificate_id': hashlib.sha256(f"{cattle_id}{time.time()}".encode()).hexdigest()
        }
        
        # Encrypt certificate
        encrypted_cert = self.cipher_suite.encrypt(json.dumps(certificate_data).encode())
        
        return {
            'certificate': base64.b64encode(encrypted_cert).decode(),
            'certificate_id': certificate_data['certificate_id'],
            'qr_code': self.generate_qr_code(certificate_data)
        }
    
    def verify_certificate(self, encrypted_certificate):
        """Verify digital certificate"""
        try:
            cert_bytes = base64.b64decode(encrypted_certificate.encode())
            decrypted_cert = self.cipher_suite.decrypt(cert_bytes)
            certificate_data = json.loads(decrypted_cert.decode())
            
            # Verify with blockchain
            verification = self.blockchain.verify_cattle_authenticity(certificate_data['cattle_id'])
            
            return {
                'valid': verification['valid'],
                'certificate_data': certificate_data,
                'blockchain_verification': verification
            }
        
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def generate_qr_code(self, certificate_data):
        """Generate QR code for certificate"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(certificate_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str

class SmartContract:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.contracts = {}
    
    def create_breeding_contract(self, contract_id, male_id, female_id, expected_date, reward):
        """Create smart contract for breeding"""
        contract = {
            'contract_id': contract_id,
            'type': 'breeding',
            'male_id': male_id,
            'female_id': female_id,
            'expected_date': expected_date,
            'reward': reward,
            'status': 'active',
            'created_date': datetime.now().isoformat()
        }
        
        self.contracts[contract_id] = contract
        
        # Add to blockchain
        transaction = Transaction(
            from_address="system",
            to_address=contract_id,
            amount=0,
            transaction_type="smart_contract",
            data=contract
        )
        
        self.blockchain.add_transaction(transaction)
        return contract
    
    def execute_breeding_contract(self, contract_id, offspring_id):
        """Execute breeding contract when offspring is born"""
        if contract_id not in self.contracts:
            return False
        
        contract = self.contracts[contract_id]
        if contract['status'] != 'active':
            return False
        
        # Register offspring
        offspring_data = {
            'cattle_id': offspring_id,
            'breed': 'Mixed',  # Determine from parents
            'birth_date': datetime.now().isoformat(),
            'owner_id': contract.get('owner_id', 'farm_owner'),
            'farm_location': 'Smart Farm',
            'parent_ids': [contract['male_id'], contract['female_id']]
        }
        
        self.blockchain.register_cattle(offspring_data)
        
        # Update contract
        contract['status'] = 'completed'
        contract['offspring_id'] = offspring_id
        contract['completion_date'] = datetime.now().isoformat()
        
        return True

def create_blockchain_api():
    """Create REST API for blockchain operations"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    blockchain = CattleBlockchain()
    certification = CattleCertification(blockchain)
    smart_contracts = SmartContract(blockchain)
    
    @app.route('/register_cattle', methods=['POST'])
    def register_cattle():
        data = request.json
        transaction = blockchain.register_cattle(data)
        blockchain.mine_pending_transactions("system")
        
        return jsonify({
            'success': True,
            'transaction_id': transaction.transaction_id,
            'message': 'Cattle registered successfully'
        })
    
    @app.route('/verify_cattle/<cattle_id>', methods=['GET'])
    def verify_cattle(cattle_id):
        verification = blockchain.verify_cattle_authenticity(cattle_id)
        return jsonify(verification)
    
    @app.route('/transfer_ownership', methods=['POST'])
    def transfer_ownership():
        data = request.json
        transaction = blockchain.transfer_ownership(
            data['cattle_id'],
            data['from_owner'],
            data['to_owner'],
            data.get('price', 0)
        )
        blockchain.mine_pending_transactions("system")
        
        return jsonify({
            'success': True,
            'transaction_id': transaction.transaction_id
        })
    
    @app.route('/generate_certificate/<cattle_id>', methods=['GET'])
    def generate_certificate(cattle_id):
        certificate = certification.generate_certificate(cattle_id)
        if certificate:
            return jsonify(certificate)
        else:
            return jsonify({'error': 'Cannot generate certificate'}), 400
    
    @app.route('/blockchain_status', methods=['GET'])
    def blockchain_status():
        return jsonify({
            'chain_length': len(blockchain.chain),
            'pending_transactions': len(blockchain.pending_transactions),
            'is_valid': blockchain.is_chain_valid()
        })
    
    return app

if __name__ == "__main__":
    # Initialize blockchain
    blockchain = CattleBlockchain()
    
    # Example usage
    cattle_data = {
        'cattle_id': 'COW001',
        'breed': 'Gir',
        'birth_date': '2023-01-15',
        'owner_id': 'FARMER001',
        'farm_location': 'Gujarat, India'
    }
    
    # Register cattle
    blockchain.register_cattle(cattle_data)
    blockchain.mine_pending_transactions("system")
    
    # Verify cattle
    verification = blockchain.verify_cattle_authenticity('COW001')
    print("Verification:", verification)
    
    # Start API server
    app = create_blockchain_api()
    print("🔗 Blockchain API started on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)