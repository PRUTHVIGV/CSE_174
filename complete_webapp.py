import http.server
import socketserver
import json
import urllib.parse
from user_auth import UserAuth

class CattleAIWebApp(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.auth = UserAuth()
        # Create demo users
        self.auth.register_user('demo_farmer', 'farmer@example.com', 'password123', 'farmer')
        self.auth.register_user('demo_student', 'student@example.com', 'password123', 'student')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/login':
            self.send_login_page()
        elif self.path == '/signup':
            self.send_signup_page()
        elif self.path == '/home':
            self.send_home_page()
        elif self.path == '/dashboard':
            self.send_dashboard_page()
        elif self.path == '/ai-prediction':
            self.send_ai_prediction_page()
        elif self.path == '/education':
            self.send_education_page()
        elif self.path == '/market':
            self.send_market_page()
        elif self.path == '/sih-solutions':
            self.send_sih_page()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/login':
            self.handle_login()
        elif self.path == '/api/signup':
            self.handle_signup()
        elif self.path == '/api/logout':
            self.handle_logout()
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_login_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CattleAI - Login</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        
        .logo {
            font-size: 2.5rem;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
            text-align: left;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 500;
        }
        
        .form-group input {
            width: 100%;
            padding: 1rem;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        .btn {
            width: 100%;
            padding: 1rem;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
            margin-bottom: 1rem;
        }
        
        .btn:hover {
            background: #45a049;
        }
        
        .demo-accounts {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        
        .demo-accounts h4 {
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        
        .link {
            color: #4CAF50;
            text-decoration: none;
            font-weight: 500;
        }
        
        .link:hover {
            text-decoration: underline;
        }
        
        .alert {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: none;
        }
        
        .alert.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <i class="fas fa-cow"></i> CattleAI
        </div>
        <h2 style="margin-bottom: 2rem; color: #333;">Welcome Back</h2>
        
        <div id="alert" class="alert"></div>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="btn">
                <i class="fas fa-sign-in-alt"></i> Login
            </button>
        </form>
        
        <div class="demo-accounts">
            <h4>Demo Accounts:</h4>
            <p><strong>Farmer:</strong> demo_farmer / password123</p>
            <p><strong>Student:</strong> demo_student / password123</p>
        </div>
        
        <p>Don't have an account? <a href="/signup" class="link">Sign up here</a></p>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const alertDiv = document.getElementById('alert');
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alertDiv.className = 'alert success';
                    alertDiv.style.display = 'block';
                    alertDiv.textContent = 'Login successful! Redirecting...';
                    
                    localStorage.setItem('session_token', result.session_token);
                    localStorage.setItem('user', JSON.stringify(result.user));
                    
                    setTimeout(() => {
                        window.location.href = '/home';
                    }, 1500);
                } else {
                    alertDiv.className = 'alert error';
                    alertDiv.style.display = 'block';
                    alertDiv.textContent = result.message;
                }
            } catch (error) {
                alertDiv.className = 'alert error';
                alertDiv.style.display = 'block';
                alertDiv.textContent = 'Login failed. Please try again.';
            }
        });
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_signup_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CattleAI - Sign Up</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
        }
        
        .signup-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 450px;
            text-align: center;
        }
        
        .logo {
            font-size: 2.5rem;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
            text-align: left;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #333;
            font-weight: 500;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 1rem;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #4CAF50;
        }
        
        .btn {
            width: 100%;
            padding: 1rem;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
            margin-bottom: 1rem;
        }
        
        .btn:hover {
            background: #45a049;
        }
        
        .link {
            color: #4CAF50;
            text-decoration: none;
            font-weight: 500;
        }
        
        .link:hover {
            text-decoration: underline;
        }
        
        .alert {
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            display: none;
        }
        
        .alert.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="signup-container">
        <div class="logo">
            <i class="fas fa-cow"></i> CattleAI
        </div>
        <h2 style="margin-bottom: 2rem; color: #333;">Create Account</h2>
        
        <div id="alert" class="alert"></div>
        
        <form id="signupForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="user_type">I am a:</label>
                <select id="user_type" name="user_type" required>
                    <option value="farmer">Farmer</option>
                    <option value="student">Student</option>
                    <option value="researcher">Researcher</option>
                    <option value="entrepreneur">Entrepreneur</option>
                    <option value="government">Government Official</option>
                </select>
            </div>
            
            <button type="submit" class="btn">
                <i class="fas fa-user-plus"></i> Create Account
            </button>
        </form>
        
        <p>Already have an account? <a href="/login" class="link">Login here</a></p>
    </div>
    
    <script>
        document.getElementById('signupForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            const alertDiv = document.getElementById('alert');
            
            try {
                const response = await fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alertDiv.className = 'alert success';
                    alertDiv.style.display = 'block';
                    alertDiv.textContent = 'Account created successfully! Redirecting to login...';
                    
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    alertDiv.className = 'alert error';
                    alertDiv.style.display = 'block';
                    alertDiv.textContent = result.message;
                }
            } catch (error) {
                alertDiv.className = 'alert error';
                alertDiv.style.display = 'block';
                alertDiv.textContent = 'Registration failed. Please try again.';
            }
        });
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_home_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CattleAI - Home</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .navbar {
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4CAF50;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover { color: #4CAF50; }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logout-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        
        .hero {
            padding: 120px 0 80px;
            text-align: center;
            color: white;
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-content {
            background: white;
            margin-top: -50px;
            border-radius: 20px 20px 0 0;
            position: relative;
            z-index: 10;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            text-align: center;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            font-size: 3rem;
            color: #4CAF50;
            margin-bottom: 1rem;
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }
        
        .cta-button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 1rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
        }
        
        .cta-button:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .stats-section {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            margin: 3rem 0;
            text-align: center;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            display: block;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .nav-links { display: none; }
            .features-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">
                <i class="fas fa-cow"></i>
                CattleAI
            </div>
            <ul class="nav-links">
                <li><a href="/home">Home</a></li>
                <li><a href="/dashboard">Dashboard</a></li>
                <li><a href="/ai-prediction">AI Prediction</a></li>
                <li><a href="/education">Education</a></li>
                <li><a href="/market">Market</a></li>
            </ul>
            <div class="user-info">
                <span id="username">Welcome!</span>
                <button class="logout-btn" onclick="logout()">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </button>
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-container">
            <h1>Welcome to CattleAI Platform</h1>
            <p>Your Complete Cattle Management Solution</p>
        </div>
    </section>

    <main class="main-content">
        <div class="container">
            <div class="stats-section">
                <h2>Platform Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">96.8%</span>
                        <div>AI Accuracy</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">50K+</span>
                        <div>Farmers Helped</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">10</span>
                        <div>Breeds Supported</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">24/7</span>
                        <div>Support Available</div>
                    </div>
                </div>
            </div>
            
            <h2 style="text-align: center; margin: 3rem 0; font-size: 2.5rem; color: #333;">
                Choose Your Path
            </h2>
            
            <div class="features-grid">
                <div class="feature-card" onclick="window.location.href='/ai-prediction'">
                    <div class="feature-icon"><i class="fas fa-brain"></i></div>
                    <h3>AI Breed Recognition</h3>
                    <p>Upload cattle images and get instant breed identification with 96.8% accuracy using Vision Transformers.</p>
                    <a href="/ai-prediction" class="cta-button">
                        <i class="fas fa-camera"></i> Start Recognition
                    </a>
                </div>
                
                <div class="feature-card" onclick="window.location.href='/education'">
                    <div class="feature-icon"><i class="fas fa-graduation-cap"></i></div>
                    <h3>SDG-04 Education</h3>
                    <p>Access comprehensive learning modules, courses, and certifications for cattle farming excellence.</p>
                    <a href="/education" class="cta-button">
                        <i class="fas fa-book"></i> Start Learning
                    </a>
                </div>
                
                <div class="feature-card" onclick="window.location.href='/market'">
                    <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
                    <h3>Market Intelligence</h3>
                    <p>Get real-time market prices, trends analysis, and investment recommendations for cattle trading.</p>
                    <a href="/market" class="cta-button">
                        <i class="fas fa-coins"></i> Check Prices
                    </a>
                </div>
                
                <div class="feature-card" onclick="window.location.href='/sih-solutions'">
                    <div class="feature-icon"><i class="fas fa-flag-checkered"></i></div>
                    <h3>SIH Solutions</h3>
                    <p>Explore Smart India Hackathon solutions addressing national challenges in livestock management.</p>
                    <a href="/sih-solutions" class="cta-button">
                        <i class="fas fa-lightbulb"></i> View Solutions
                    </a>
                </div>
                
                <div class="feature-card" onclick="window.location.href='/dashboard'">
                    <div class="feature-icon"><i class="fas fa-tachometer-alt"></i></div>
                    <h3>Personal Dashboard</h3>
                    <p>Track your progress, view statistics, manage your cattle records, and monitor performance.</p>
                    <a href="/dashboard" class="cta-button">
                        <i class="fas fa-chart-bar"></i> View Dashboard
                    </a>
                </div>
                
                <div class="feature-card" onclick="showPPTModal()">
                    <div class="feature-icon"><i class="fas fa-presentation"></i></div>
                    <h3>Project Presentation</h3>
                    <p>View comprehensive project presentation, technical details, and implementation roadmap.</p>
                    <button class="cta-button" onclick="showPPTModal()">
                        <i class="fas fa-play"></i> View PPT
                    </button>
                </div>
            </div>
        </div>
    </main>
    
    <!-- PPT Modal -->
    <div id="pptModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 2000; padding: 2rem;">
        <div style="background: white; border-radius: 20px; padding: 2rem; max-width: 800px; margin: 0 auto; max-height: 90vh; overflow-y: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <h2>CattleAI - Project Presentation</h2>
                <button onclick="closePPTModal()" style="background: #ff4757; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                    <i class="fas fa-times"></i> Close
                </button>
            </div>
            <div id="pptContent">
                <div style="text-align: center; margin: 2rem 0;">
                    <h3>Slide 1: Project Overview</h3>
                    <p><strong>CattleAI: Next-Generation Cattle Breed Recognition System</strong></p>
                    <p>AI-Powered Livestock Management Platform</p>
                </div>
                <div style="margin: 2rem 0;">
                    <h3>Slide 2: Problem Statement</h3>
                    <ul>
                        <li>Manual cattle identification is time-consuming and error-prone</li>
                        <li>Farmers lack access to modern cattle management techniques</li>
                        <li>Limited educational resources for livestock farming</li>
                        <li>Inefficient market price discovery</li>
                    </ul>
                </div>
                <div style="margin: 2rem 0;">
                    <h3>Slide 3: Our Solution</h3>
                    <ul>
                        <li>96.8% accurate AI breed recognition using Vision Transformers</li>
                        <li>Comprehensive education platform (SDG-04)</li>
                        <li>Real-time market intelligence</li>
                        <li>Government integration (SIH solutions)</li>
                    </ul>
                </div>
                <div style="margin: 2rem 0;">
                    <h3>Slide 4: Technical Architecture</h3>
                    <ul>
                        <li>Frontend: React/HTML5 with responsive design</li>
                        <li>Backend: Python with machine learning models</li>
                        <li>AI: Vision Transformers, Transfer Learning</li>
                        <li>Database: User authentication and data management</li>
                    </ul>
                </div>
                <div style="margin: 2rem 0;">
                    <h3>Slide 5: Impact & Future</h3>
                    <ul>
                        <li>50,000+ farmers to be benefited</li>
                        <li>40% increase in farming efficiency</li>
                        <li>SDG alignment: Quality Education, No Poverty</li>
                        <li>Scalable to national level deployment</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Check if user is logged in
        const sessionToken = localStorage.getItem('session_token');
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        
        if (!sessionToken) {
            window.location.href = '/login';
        } else {
            document.getElementById('username').textContent = `Welcome, ${user.username}!`;
        }
        
        function logout() {
            localStorage.removeItem('session_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        
        function showPPTModal() {
            document.getElementById('pptModal').style.display = 'block';
        }
        
        function closePPTModal() {
            document.getElementById('pptModal').style.display = 'none';
        }
        
        // Close modal when clicking outside
        document.getElementById('pptModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closePPTModal();
            }
        });
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.auth.login_user(data['username'], data['password'])
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def handle_signup(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        result = self.auth.register_user(
            data['username'], 
            data['email'], 
            data['password'], 
            data['user_type']
        )
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

PORT = 8100
print("=" * 70)
print("CATTLEAI - COMPLETE WEB APPLICATION")
print("=" * 70)
print(f"Application URL: http://localhost:{PORT}")
print(f"Features: Login/Signup, Home, Dashboard, AI Prediction, Education")
print(f"Demo Accounts: demo_farmer/password123, demo_student/password123")
print("=" * 70)

with socketserver.TCPServer(("", PORT), CattleAIWebApp) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped successfully!")
        print("Thank you for using CattleAI!")