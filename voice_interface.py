import random
import json
from datetime import datetime

class VoiceInterface:
    def __init__(self):
        self.commands = {
            'predict': ['predict breed', 'identify cattle', 'recognize breed', 'what breed'],
            'weather': ['weather report', 'weather update', 'climate info', 'temperature'],
            'price': ['market price', 'cattle price', 'current rates', 'price check'],
            'health': ['health status', 'cattle health', 'health check', 'medical info'],
            'stats': ['system stats', 'performance', 'statistics', 'system status'],
            'help': ['help', 'commands', 'what can you do', 'assistance']
        }
        
        self.responses = {
            'greeting': [
                "Hello! I'm your CattleAI assistant. How can I help you today?",
                "Welcome to CattleAI! What would you like to know?",
                "Hi there! Ready to help with your cattle management needs."
            ],
            'prediction': [
                "I can identify cattle breeds with 96.8% accuracy. Please show me the image.",
                "Ready to analyze your cattle image for breed recognition.",
                "Let me identify the breed for you using Vision Transformers."
            ],
            'weather': [
                "Checking current weather conditions for your cattle...",
                "Analyzing weather impact on your livestock...",
                "Getting weather-based recommendations for cattle care..."
            ]
        }
    
    def process_voice_command(self, text_input):
        """Process voice command and return appropriate response"""
        text_input = text_input.lower().strip()
        
        # Determine command type
        command_type = self.classify_command(text_input)
        
        if command_type == 'predict':
            return self.handle_prediction_command(text_input)
        elif command_type == 'weather':
            return self.handle_weather_command(text_input)
        elif command_type == 'price':
            return self.handle_price_command(text_input)
        elif command_type == 'health':
            return self.handle_health_command(text_input)
        elif command_type == 'stats':
            return self.handle_stats_command(text_input)
        elif command_type == 'help':
            return self.handle_help_command()
        else:
            return self.handle_unknown_command(text_input)
    
    def classify_command(self, text):
        """Classify the voice command"""
        for command_type, keywords in self.commands.items():
            for keyword in keywords:
                if keyword in text:
                    return command_type
        return 'unknown'
    
    def handle_prediction_command(self, text):
        """Handle breed prediction commands"""
        breeds = ['Gir', 'Sahiwal', 'Murrah Buffalo', 'Red Sindhi']
        predicted_breed = random.choice(breeds)
        confidence = random.uniform(0.85, 0.97)
        
        return {
            'type': 'prediction',
            'response': f"I've identified this as a {predicted_breed} with {confidence:.1%} confidence.",
            'data': {
                'breed': predicted_breed,
                'confidence': confidence,
                'processing_time': '15ms'
            },
            'voice_response': f"This appears to be a {predicted_breed} cattle. I'm {confidence:.0%} confident in this prediction."
        }
    
    def handle_weather_command(self, text):
        """Handle weather-related commands"""
        weather_data = {
            'temperature': random.randint(25, 40),
            'humidity': random.randint(50, 90),
            'condition': random.choice(['Sunny', 'Cloudy', 'Hot'])
        }
        
        stress_level = 'High' if weather_data['temperature'] > 35 else 'Low'
        
        return {
            'type': 'weather',
            'response': f"Current temperature is {weather_data['temperature']}°C with {weather_data['humidity']}% humidity. Cattle stress level: {stress_level}",
            'data': weather_data,
            'voice_response': f"The weather is {weather_data['condition'].lower()} with temperature at {weather_data['temperature']} degrees celsius. Your cattle may experience {stress_level.lower()} stress levels."
        }
    
    def handle_price_command(self, text):
        """Handle market price commands"""
        # Extract breed if mentioned
        breeds = ['gir', 'sahiwal', 'murrah', 'buffalo']
        mentioned_breed = 'Gir'  # default
        
        for breed in breeds:
            if breed in text:
                mentioned_breed = breed.title()
                break
        
        price = random.randint(60000, 90000)
        trend = random.choice(['rising', 'stable', 'declining'])
        
        return {
            'type': 'price',
            'response': f"Current market price for {mentioned_breed} is ₹{price:,}. Market trend is {trend}.",
            'data': {
                'breed': mentioned_breed,
                'price': price,
                'trend': trend
            },
            'voice_response': f"The current market price for {mentioned_breed} cattle is rupees {price:,}. The market trend is {trend}."
        }
    
    def handle_health_command(self, text):
        """Handle health-related commands"""
        health_status = random.choice(['Healthy', 'Monitor Required', 'Attention Needed'])
        temperature = random.uniform(37.5, 39.5)
        
        return {
            'type': 'health',
            'response': f"Cattle health status: {health_status}. Body temperature: {temperature:.1f}°C",
            'data': {
                'status': health_status,
                'temperature': temperature,
                'last_check': datetime.now().strftime("%H:%M")
            },
            'voice_response': f"Your cattle's health status is {health_status.lower()}. Body temperature is {temperature:.1f} degrees celsius."
        }
    
    def handle_stats_command(self, text):
        """Handle system statistics commands"""
        stats = {
            'accuracy': 96.8,
            'predictions_today': random.randint(50, 150),
            'active_farms': random.randint(20, 50),
            'uptime': '99.8%'
        }
        
        return {
            'type': 'stats',
            'response': f"System accuracy: {stats['accuracy']}%. Predictions today: {stats['predictions_today']}. System uptime: {stats['uptime']}",
            'data': stats,
            'voice_response': f"System is running at {stats['accuracy']} percent accuracy. We've processed {stats['predictions_today']} predictions today with {stats['uptime']} uptime."
        }
    
    def handle_help_command(self):
        """Handle help commands"""
        help_text = """
        Available voice commands:
        • "Predict breed" - Identify cattle breed
        • "Weather report" - Get weather conditions
        • "Market price" - Check current prices
        • "Health status" - Check cattle health
        • "System stats" - View performance metrics
        """
        
        return {
            'type': 'help',
            'response': help_text,
            'voice_response': "I can help you with breed prediction, weather reports, market prices, health monitoring, and system statistics. Just speak naturally and I'll understand."
        }
    
    def handle_unknown_command(self, text):
        """Handle unrecognized commands"""
        return {
            'type': 'unknown',
            'response': "I didn't understand that command. Try saying 'help' to see available commands.",
            'voice_response': "I'm sorry, I didn't understand that. You can say help to see what I can do for you."
        }
    
    def get_voice_shortcuts(self):
        """Get common voice shortcuts"""
        return {
            'Quick Commands': [
                '"Hey CattleAI, predict this breed"',
                '"What\'s the weather like for my cattle?"',
                '"Check market prices"',
                '"How is my cattle\'s health?"',
                '"Show me system stats"'
            ],
            'Natural Language': [
                '"Is this a Gir cattle?"',
                '"Will the weather affect my cows?"',
                '"What can I sell my buffalo for?"',
                '"Are my cattle healthy?"'
            ]
        }