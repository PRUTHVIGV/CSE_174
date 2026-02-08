import http.server
import socketserver
import json
import random
from sdg_education import EducationModule
from sih_solution import SIHSolutionModule

class SDGSIHHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.education = EducationModule()
        self.sih = SIHSolutionModule()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.send_sdg_sih_page()
        elif self.path == '/api/education':
            self.send_education_data()
        elif self.path == '/api/sih':
            self.send_sih_data()
        elif self.path == '/api/impact':
            self.send_impact_metrics()
        else:
            super().do_GET()
    
    def send_sdg_sih_page(self):
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CattleAI - SDG & SIH Solution Platform</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
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
        
        .hero {
            padding: 120px 0 80px;
            text-align: center;
            color: white;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .sdg-badges {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .sdg-badge {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
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
        
        .section {
            margin-bottom: 4rem;
        }
        
        .section-title {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 3rem;
            color: #333;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid rgba(0,0,0,0.05);
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
        
        .sdg-section {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            margin: 3rem 0;
        }
        
        .sih-section {
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            margin: 3rem 0;
        }
        
        .demo-button {
            background: white;
            color: #4CAF50;
            border: none;
            padding: 1rem 2rem;
            font-size: 1rem;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.5rem;
        }
        
        .demo-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .demo-button.sih {
            color: #FF6B35;
        }
        
        .impact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .impact-card {
            text-align: center;
            padding: 1.5rem;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .impact-number {
            font-size: 2rem;
            font-weight: bold;
            display: block;
            margin-bottom: 0.5rem;
        }
        
        .result-container {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .problem-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .problem-card {
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .features-grid { grid-template-columns: 1fr; }
            .sdg-badges { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">
                <i class="fas fa-graduation-cap"></i>
                CattleAI - SDG & SIH Platform
            </div>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-container">
            <h1><i class="fas fa-globe"></i> Sustainable Development Goals</h1>
            <p>AI-Powered Solutions for Quality Education & Smart India</p>
            <div class="sdg-badges">
                <div class="sdg-badge">SDG-01: No Poverty</div>
                <div class="sdg-badge">SDG-02: Zero Hunger</div>
                <div class="sdg-badge">SDG-04: Quality Education</div>
                <div class="sdg-badge">SDG-08: Decent Work</div>
                <div class="sdg-badge">SDG-09: Innovation</div>
            </div>
        </div>
    </section>

    <main class="main-content">
        <div class="container">
            <section class="section">
                <h2 class="section-title">SDG & SIH Integration</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon"><i class="fas fa-graduation-cap"></i></div>
                        <h3>SDG-04: Quality Education</h3>
                        <p>Comprehensive digital learning platform for cattle farming education, skill development, and knowledge sharing.</p>
                        <ul style="margin-top: 1rem; color: #666;">
                            <li>• Multi-language learning modules</li>
                            <li>• Interactive AI-powered lessons</li>
                            <li>• Digital certificates & credentials</li>
                            <li>• Peer-to-peer learning network</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon"><i class="fas fa-lightbulb"></i></div>
                        <h3>Smart India Hackathon</h3>
                        <p>Government-focused solutions addressing national challenges in livestock management and farmer welfare.</p>
                        <ul style="margin-top: 1rem; color: #666;">
                            <li>• Automated livestock census</li>
                            <li>• Farmer income doubling</li>
                            <li>• Food security solutions</li>
                            <li>• Rural employment generation</li>
                        </ul>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
                        <h3>Social Impact Measurement</h3>
                        <p>Comprehensive tracking and measurement of social, economic, and environmental impact metrics.</p>
                        <ul style="margin-top: 1rem; color: #666;">
                            <li>• Farmer income tracking</li>
                            <li>• Education completion rates</li>
                            <li>• Employment generation metrics</li>
                            <li>• Sustainability indicators</li>
                        </ul>
                    </div>
                </div>
            </section>

            <section class="sdg-section">
                <h2><i class="fas fa-book"></i> SDG-04: Quality Education Platform</h2>
                <p>Empowering farmers through accessible, technology-enabled education</p>
                
                <div class="impact-grid">
                    <div class="impact-card">
                        <span class="impact-number">50,000+</span>
                        <div>Farmers Educated</div>
                    </div>
                    <div class="impact-card">
                        <span class="impact-number">12</span>
                        <div>Languages Supported</div>
                    </div>
                    <div class="impact-card">
                        <span class="impact-number">95%</span>
                        <div>Course Completion Rate</div>
                    </div>
                    <div class="impact-card">
                        <span class="impact-number">40%</span>
                        <div>Income Increase</div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <button class="demo-button" onclick="showEducationDemo()">
                        <i class="fas fa-play"></i> Launch Learning Platform
                    </button>
                    <button class="demo-button" onclick="showCertificateDemo()">
                        <i class="fas fa-certificate"></i> Generate Certificate
                    </button>
                </div>
                
                <div id="education-result"></div>
            </section>

            <section class="sih-section">
                <h2><i class="fas fa-flag-checkered"></i> Smart India Hackathon Solutions</h2>
                <p>Addressing national challenges through innovative AI solutions</p>
                
                <div class="problem-cards">
                    <div class="problem-card">
                        <h4><i class="fas fa-clipboard-list"></i> Livestock Census</h4>
                        <p>Automated cattle counting and breed identification for accurate government records</p>
                        <small>Ministry: Agriculture & Farmers Welfare</small>
                    </div>
                    <div class="problem-card">
                        <h4><i class="fas fa-coins"></i> Farmer Income</h4>
                        <p>AI-powered cattle management to double farmer income through technology</p>
                        <small>Ministry: Agriculture & Farmers Welfare</small>
                    </div>
                    <div class="problem-card">
                        <h4><i class="fas fa-seedling"></i> Food Security</h4>
                        <p>Optimize dairy production to meet growing food demand</p>
                        <small>Ministry: Consumer Affairs & Food</small>
                    </div>
                    <div class="problem-card">
                        <h4><i class="fas fa-users"></i> Rural Employment</h4>
                        <p>Generate employment opportunities through agri-tech adoption</p>
                        <small>Ministry: Rural Development</small>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <button class="demo-button sih" onclick="showSIHProposal()">
                        <i class="fas fa-file-alt"></i> View SIH Proposal
                    </button>
                    <button class="demo-button sih" onclick="showImpactMetrics()">
                        <i class="fas fa-chart-bar"></i> Impact Analysis
                    </button>
                    <button class="demo-button sih" onclick="showPitchDeck()">
                        <i class="fas fa-presentation"></i> Pitch Deck
                    </button>
                </div>
                
                <div id="sih-result"></div>
            </section>
        </div>
    </main>

    <script>
        function showEducationDemo() {
            const resultDiv = document.getElementById('education-result');
            resultDiv.innerHTML = '<div class="loading"></div> Loading personalized learning path...';
            
            setTimeout(() => {
                resultDiv.innerHTML = `
                    <div class="result-container">
                        <h3><i class="fas fa-graduation-cap" style="color: #4CAF50;"></i> Personalized Learning Path</h3>
                        <div style="margin-top: 1rem;">
                            <h4>Recommended Courses for New Farmer:</h4>
                            <ul style="text-align: left; margin: 1rem 0;">
                                <li><strong>Basic Cattle Care & Management</strong> - 2 weeks (Hindi/English)</li>
                                <li><strong>Indian Cattle Breed Identification</strong> - 1 week (Hindi/English)</li>
                                <li><strong>Financial Management for Farmers</strong> - 2 weeks (Hindi/English)</li>
                            </ul>
                            <p><strong>Total Duration:</strong> 5 weeks</p>
                            <p><strong>SDG Alignment:</strong> SDG-04 Quality Education for Sustainable Agriculture</p>
                            <p><strong>Expected Outcome:</strong> 40% increase in farming efficiency</p>
                        </div>
                    </div>
                `;
            }, 2000);
        }
        
        function showCertificateDemo() {
            const resultDiv = document.getElementById('education-result');
            resultDiv.innerHTML = '<div class="loading"></div> Generating digital certificate...';
            
            setTimeout(() => {
                const certId = 'CATTLE-EDU-' + Math.floor(Math.random() * 90000 + 10000);
                resultDiv.innerHTML = `
                    <div class="result-container">
                        <h3><i class="fas fa-certificate" style="color: #FFD700;"></i> Digital Certificate Generated</h3>
                        <div style="margin-top: 1rem; text-align: left;">
                            <p><strong>Certificate ID:</strong> ${certId}</p>
                            <p><strong>Course:</strong> Basic Cattle Care & Management</p>
                            <p><strong>Student:</strong> Ramesh Kumar</p>
                            <p><strong>Score:</strong> 92% (Grade A)</p>
                            <p><strong>Completion Date:</strong> ${new Date().toLocaleDateString()}</p>
                            <p><strong>Skills Acquired:</strong> Feeding, Housing, Health Care, Breeding</p>
                            <p><strong>Blockchain Verified:</strong> ✅ Yes</p>
                            <p><strong>SDG Contribution:</strong> Contributing to SDG-04: Quality Education</p>
                        </div>
                    </div>
                `;
            }, 1800);
        }
        
        function showSIHProposal() {
            const resultDiv = document.getElementById('sih-result');
            resultDiv.innerHTML = '<div class="loading"></div> Generating SIH proposal...';
            
            setTimeout(() => {
                resultDiv.innerHTML = `
                    <div class="result-container">
                        <h3><i class="fas fa-file-alt" style="color: #FF6B35;"></i> SIH Problem Statement Solution</h3>
                        <div style="margin-top: 1rem; text-align: left;">
                            <h4>Problem: Automated Livestock Census for Government</h4>
                            <p><strong>Ministry:</strong> Agriculture & Farmers Welfare</p>
                            <p><strong>Current Challenge:</strong> Manual livestock counting is 60% accurate, time-consuming</p>
                            <p><strong>Our Solution:</strong> AI-powered breed recognition with 96.8% accuracy</p>
                            
                            <h4 style="margin-top: 1rem;">Technical Architecture:</h4>
                            <ul>
                                <li>Frontend: React Native Mobile App + Web Dashboard</li>
                                <li>AI Models: Vision Transformers, Object Detection</li>
                                <li>Database: MongoDB + Blockchain (Hyperledger)</li>
                                <li>Cloud: AWS/Azure Government Cloud</li>
                            </ul>
                            
                            <h4 style="margin-top: 1rem;">Expected Impact:</h4>
                            <ul>
                                <li>10 million+ farmers benefited</li>
                                <li>95% accuracy vs 60% manual</li>
                                <li>₹500 crores annual cost savings</li>
                                <li>50,000 jobs created</li>
                            </ul>
                        </div>
                    </div>
                `;
            }, 2500);
        }
        
        function showImpactMetrics() {
            const resultDiv = document.getElementById('sih-result');
            resultDiv.innerHTML = '<div class="loading"></div> Calculating social impact...';
            
            setTimeout(() => {
                resultDiv.innerHTML = `
                    <div class="result-container">
                        <h3><i class="fas fa-chart-bar" style="color: #FF6B35;"></i> Social Impact Analysis</h3>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                <div style="font-size: 1.5rem; font-weight: bold;">10M+</div>
                                <div>Farmers Benefited</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                <div style="font-size: 1.5rem; font-weight: bold;">₹500Cr</div>
                                <div>Annual Savings</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                <div style="font-size: 1.5rem; font-weight: bold;">50K</div>
                                <div>Jobs Created</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                                <div style="font-size: 1.5rem; font-weight: bold;">95%</div>
                                <div>Accuracy Achieved</div>
                            </div>
                        </div>
                        <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                            <strong>SDG Alignment:</strong><br>
                            SDG-1: No Poverty • SDG-2: Zero Hunger • SDG-4: Quality Education • SDG-8: Decent Work
                        </div>
                    </div>
                `;
            }, 2000);
        }
        
        function showPitchDeck() {
            const resultDiv = document.getElementById('sih-result');
            resultDiv.innerHTML = '<div class="loading"></div> Preparing pitch presentation...';
            
            setTimeout(() => {
                resultDiv.innerHTML = `
                    <div class="result-container">
                        <h3><i class="fas fa-presentation" style="color: #FF6B35;"></i> SIH Pitch Deck</h3>
                        <div style="margin-top: 1rem; text-align: left;">
                            <h4>Slide 1: CattleAI - Automated Livestock Census</h4>
                            <p>AI-powered solution for accurate government livestock records</p>
                            
                            <h4 style="margin-top: 1rem;">Slide 2: Problem Statement</h4>
                            <ul>
                                <li>300 million cattle in India</li>
                                <li>40% accuracy in manual census</li>
                                <li>₹2.5 lakh crore livestock economy</li>
                                <li>Outdated data affects policy making</li>
                            </ul>
                            
                            <h4 style="margin-top: 1rem;">Slide 3: Our Solution</h4>
                            <ul>
                                <li>96.8% AI accuracy in breed recognition</li>
                                <li>Real-time data collection and analysis</li>
                                <li>Government system integration</li>
                                <li>Mobile and web applications</li>
                            </ul>
                            
                            <h4 style="margin-top: 1rem;">Slide 4: Market Opportunity</h4>
                            <p>₹2.5 lakh crore livestock market • 15% annual growth • Government partnership potential</p>
                            
                            <h4 style="margin-top: 1rem;">Slide 5: Ask</h4>
                            <p>Seeking government partnership for nationwide deployment and ₹10 crore funding</p>
                        </div>
                    </div>
                `;
            }, 2200);
        }
        
        // Auto-run education demo on page load
        setTimeout(() => {
            showEducationDemo();
        }, 3000);
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_education_data(self):
        user_profile = {'experience': 'new', 'role': 'farmer', 'language': 'Hindi'}
        learning_path = self.education.get_personalized_learning_path(user_profile)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(learning_path).encode())
    
    def send_sih_data(self):
        proposal = self.sih.generate_sih_proposal('livestock_census')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(proposal).encode())

PORT = 8090
print("=" * 70)
print("CATTLEAI - SDG & SIH SOLUTION PLATFORM")
print("=" * 70)
print(f"SDG-04 Education Platform: http://localhost:{PORT}")
print(f"Smart India Hackathon Solutions: Integrated")
print(f"Social Impact Tracking: Active")
print("=" * 70)

with socketserver.TCPServer(("", PORT), SDGSIHHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped successfully!")
        print("Thank you for supporting SDG and SIH initiatives!")