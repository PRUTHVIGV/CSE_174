import json
import hashlib
import random
import string
from datetime import datetime

class UserAuth:
    def __init__(self):
        self.users_db = {}  # In production, use proper database
        self.sessions = {}
        
    def hash_password(self, password):
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_session_token(self):
        """Generate secure session token"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    def register_user(self, username, email, password, user_type='farmer'):
        """Register new user"""
        if username in self.users_db:
            return {'success': False, 'message': 'Username already exists'}
        
        if any(user['email'] == email for user in self.users_db.values()):
            return {'success': False, 'message': 'Email already registered'}
        
        user_id = f"USER_{len(self.users_db) + 1:04d}"
        
        self.users_db[username] = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'password': self.hash_password(password),
            'user_type': user_type,
            'created_at': datetime.now().isoformat(),
            'profile': {
                'full_name': '',
                'location': '',
                'farm_size': '',
                'cattle_count': 0,
                'experience': 'beginner'
            },
            'stats': {
                'predictions_made': 0,
                'courses_completed': 0,
                'certificates_earned': 0,
                'last_login': None
            }
        }
        
        return {'success': True, 'message': 'Registration successful', 'user_id': user_id}
    
    def login_user(self, username, password):
        """Authenticate user login"""
        if username not in self.users_db:
            return {'success': False, 'message': 'Invalid username or password'}
        
        user = self.users_db[username]
        if user['password'] != self.hash_password(password):
            return {'success': False, 'message': 'Invalid username or password'}
        
        # Generate session token
        session_token = self.generate_session_token()
        self.sessions[session_token] = {
            'username': username,
            'login_time': datetime.now().isoformat(),
            'user_type': user['user_type']
        }
        
        # Update last login
        user['stats']['last_login'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'message': 'Login successful',
            'session_token': session_token,
            'user': {
                'username': username,
                'user_type': user['user_type'],
                'user_id': user['user_id']
            }
        }
    
    def verify_session(self, session_token):
        """Verify user session"""
        if session_token not in self.sessions:
            return {'valid': False, 'message': 'Invalid session'}
        
        session = self.sessions[session_token]
        username = session['username']
        
        if username not in self.users_db:
            return {'valid': False, 'message': 'User not found'}
        
        return {
            'valid': True,
            'user': self.users_db[username],
            'session': session
        }
    
    def logout_user(self, session_token):
        """Logout user and invalidate session"""
        if session_token in self.sessions:
            del self.sessions[session_token]
            return {'success': True, 'message': 'Logged out successfully'}
        return {'success': False, 'message': 'Invalid session'}
    
    def update_user_stats(self, username, stat_type, increment=1):
        """Update user statistics"""
        if username in self.users_db:
            if stat_type in self.users_db[username]['stats']:
                self.users_db[username]['stats'][stat_type] += increment
                return True
        return False
    
    def get_user_dashboard_data(self, username):
        """Get user dashboard data"""
        if username not in self.users_db:
            return None
        
        user = self.users_db[username]
        
        # Generate some sample achievements
        achievements = []
        if user['stats']['predictions_made'] >= 10:
            achievements.append({'title': 'AI Expert', 'description': '10+ predictions made'})
        if user['stats']['courses_completed'] >= 3:
            achievements.append({'title': 'Learning Champion', 'description': '3+ courses completed'})
        
        return {
            'user_info': {
                'username': user['username'],
                'user_type': user['user_type'],
                'member_since': user['created_at'][:10]
            },
            'stats': user['stats'],
            'achievements': achievements,
            'recent_activity': [
                {'action': 'Completed breed identification', 'time': '2 hours ago'},
                {'action': 'Started new course', 'time': '1 day ago'},
                {'action': 'Made AI prediction', 'time': '3 days ago'}
            ]
        }