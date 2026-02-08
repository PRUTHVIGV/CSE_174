import requests
import json
import random
from datetime import datetime

class WeatherIntegration:
    def __init__(self):
        self.weather_data = {
            'temperature': random.randint(20, 40),
            'humidity': random.randint(40, 90),
            'wind_speed': random.randint(5, 25),
            'condition': random.choice(['Sunny', 'Cloudy', 'Rainy', 'Hot'])
        }
    
    def get_weather_impact(self, breed, location="India"):
        """Get weather impact on cattle breed"""
        weather = self.weather_data
        
        # Breed-specific weather tolerance
        breed_tolerance = {
            'Gir': {'heat_tolerance': 'High', 'humidity_tolerance': 'High'},
            'Sahiwal': {'heat_tolerance': 'High', 'humidity_tolerance': 'Medium'},
            'Murrah_Buffalo': {'heat_tolerance': 'Medium', 'humidity_tolerance': 'High'},
            'Red_Sindhi': {'heat_tolerance': 'High', 'humidity_tolerance': 'Medium'}
        }
        
        tolerance = breed_tolerance.get(breed, {'heat_tolerance': 'Medium', 'humidity_tolerance': 'Medium'})
        
        # Calculate stress level
        stress_level = self.calculate_stress_level(weather, tolerance)
        
        return {
            'current_weather': weather,
            'breed_tolerance': tolerance,
            'stress_level': stress_level,
            'recommendations': self.get_recommendations(stress_level, weather),
            'milk_yield_impact': self.calculate_milk_impact(stress_level),
            'health_alerts': self.generate_health_alerts(stress_level, weather)
        }
    
    def calculate_stress_level(self, weather, tolerance):
        """Calculate cattle stress level based on weather"""
        stress_score = 0
        
        # Temperature stress
        if weather['temperature'] > 35:
            if tolerance['heat_tolerance'] == 'Low':
                stress_score += 3
            elif tolerance['heat_tolerance'] == 'Medium':
                stress_score += 2
            else:
                stress_score += 1
        
        # Humidity stress
        if weather['humidity'] > 80:
            if tolerance['humidity_tolerance'] == 'Low':
                stress_score += 2
            elif tolerance['humidity_tolerance'] == 'Medium':
                stress_score += 1
        
        if stress_score >= 4:
            return 'High'
        elif stress_score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def get_recommendations(self, stress_level, weather):
        """Get weather-based recommendations"""
        recommendations = []
        
        if stress_level == 'High':
            recommendations.extend([
                'Provide extra shade and ventilation',
                'Increase water availability',
                'Adjust feeding schedule to cooler hours',
                'Monitor cattle closely for heat stress'
            ])
        elif stress_level == 'Medium':
            recommendations.extend([
                'Ensure adequate shade',
                'Check water supply regularly',
                'Consider cooling systems'
            ])
        
        if weather['condition'] == 'Rainy':
            recommendations.append('Ensure dry shelter and proper drainage')
        
        return recommendations
    
    def calculate_milk_impact(self, stress_level):
        """Calculate impact on milk yield"""
        impact = {
            'Low': {'reduction': '0-5%', 'quality': 'Normal'},
            'Medium': {'reduction': '5-15%', 'quality': 'Slightly affected'},
            'High': {'reduction': '15-30%', 'quality': 'Significantly affected'}
        }
        return impact.get(stress_level, impact['Low'])
    
    def generate_health_alerts(self, stress_level, weather):
        """Generate health alerts based on weather"""
        alerts = []
        
        if stress_level == 'High':
            alerts.append('⚠️ HIGH HEAT STRESS ALERT')
        
        if weather['temperature'] > 38:
            alerts.append('🌡️ Extreme temperature warning')
        
        if weather['humidity'] > 85:
            alerts.append('💧 High humidity alert')
        
        return alerts