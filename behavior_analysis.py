import random
import numpy as np
from datetime import datetime, timedelta

class BehaviorAnalyzer:
    def __init__(self):
        self.behavior_patterns = {
            'eating': {'normal_duration': 6, 'frequency': 8},
            'resting': {'normal_duration': 12, 'frequency': 4},
            'walking': {'normal_duration': 4, 'frequency': 6},
            'drinking': {'normal_duration': 0.5, 'frequency': 12},
            'socializing': {'normal_duration': 2, 'frequency': 3}
        }
        
        self.health_indicators = {
            'eating_reduced': 'Possible illness or stress',
            'excessive_resting': 'May indicate fatigue or illness',
            'restlessness': 'Could be heat stress or discomfort',
            'isolation': 'Potential health or social issues',
            'aggressive': 'Stress or territorial behavior'
        }
    
    def analyze_behavior(self, cattle_id, observation_hours=24):
        """Analyze cattle behavior patterns"""
        # Simulate behavior data
        behaviors = self.generate_behavior_data(observation_hours)
        
        # Analyze patterns
        analysis = self.evaluate_behavior_patterns(behaviors)
        
        # Generate alerts
        alerts = self.generate_behavior_alerts(analysis)
        
        return {
            'cattle_id': cattle_id,
            'observation_period': f"{observation_hours} hours",
            'behaviors': behaviors,
            'analysis': analysis,
            'alerts': alerts,
            'health_score': self.calculate_health_score(analysis),
            'recommendations': self.get_behavior_recommendations(analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_behavior_data(self, hours):
        """Generate simulated behavior data"""
        behaviors = {}
        
        for behavior, pattern in self.behavior_patterns.items():
            # Add some randomness to simulate real behavior
            duration_variation = random.uniform(0.7, 1.3)
            frequency_variation = random.uniform(0.8, 1.2)
            
            actual_duration = pattern['normal_duration'] * duration_variation
            actual_frequency = int(pattern['frequency'] * frequency_variation)
            
            behaviors[behavior] = {
                'total_duration': round(actual_duration, 1),
                'frequency': actual_frequency,
                'average_session': round(actual_duration / max(actual_frequency, 1), 1),
                'percentage_of_day': round((actual_duration / hours) * 100, 1)
            }
        
        return behaviors
    
    def evaluate_behavior_patterns(self, behaviors):
        """Evaluate if behavior patterns are normal"""
        analysis = {}
        
        for behavior, data in behaviors.items():
            normal_pattern = self.behavior_patterns[behavior]
            
            # Check duration
            duration_ratio = data['total_duration'] / normal_pattern['normal_duration']
            
            # Check frequency
            frequency_ratio = data['frequency'] / normal_pattern['frequency']
            
            # Determine status
            if 0.8 <= duration_ratio <= 1.2 and 0.8 <= frequency_ratio <= 1.2:
                status = 'Normal'
            elif duration_ratio < 0.6 or frequency_ratio < 0.6:
                status = 'Below Normal'
            elif duration_ratio > 1.4 or frequency_ratio > 1.4:
                status = 'Above Normal'
            else:
                status = 'Slightly Abnormal'
            
            analysis[behavior] = {
                'status': status,
                'duration_ratio': round(duration_ratio, 2),
                'frequency_ratio': round(frequency_ratio, 2),
                'concern_level': self.get_concern_level(status)
            }
        
        return analysis
    
    def get_concern_level(self, status):
        """Get concern level based on behavior status"""
        concern_levels = {
            'Normal': 'None',
            'Slightly Abnormal': 'Low',
            'Below Normal': 'Medium',
            'Above Normal': 'Medium'
        }
        return concern_levels.get(status, 'Low')
    
    def generate_behavior_alerts(self, analysis):
        """Generate alerts based on behavior analysis"""
        alerts = []
        
        for behavior, data in analysis.items():
            if data['concern_level'] in ['Medium', 'High']:
                if behavior == 'eating' and data['status'] == 'Below Normal':
                    alerts.append({
                        'type': 'warning',
                        'message': f"Reduced eating behavior detected - {self.health_indicators.get('eating_reduced', 'Monitor closely')}",
                        'severity': 'Medium',
                        'behavior': behavior
                    })
                
                elif behavior == 'resting' and data['status'] == 'Above Normal':
                    alerts.append({
                        'type': 'warning',
                        'message': f"Excessive resting observed - {self.health_indicators.get('excessive_resting', 'Check health')}",
                        'severity': 'Medium',
                        'behavior': behavior
                    })
                
                elif behavior == 'walking' and data['status'] == 'Above Normal':
                    alerts.append({
                        'type': 'info',
                        'message': f"Increased activity detected - {self.health_indicators.get('restlessness', 'Monitor for stress')}",
                        'severity': 'Low',
                        'behavior': behavior
                    })
        
        return alerts
    
    def calculate_health_score(self, analysis):
        """Calculate overall health score based on behavior"""
        total_score = 0
        behavior_count = len(analysis)
        
        for behavior, data in analysis.items():
            if data['status'] == 'Normal':
                score = 100
            elif data['status'] == 'Slightly Abnormal':
                score = 80
            elif data['concern_level'] == 'Medium':
                score = 60
            else:
                score = 40
            
            total_score += score
        
        overall_score = total_score / behavior_count if behavior_count > 0 else 0
        
        return {
            'score': round(overall_score, 1),
            'grade': self.get_health_grade(overall_score),
            'status': self.get_health_status(overall_score)
        }
    
    def get_health_grade(self, score):
        """Get health grade based on score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_health_status(self, score):
        """Get health status based on score"""
        if score >= 90:
            return 'Excellent'
        elif score >= 80:
            return 'Good'
        elif score >= 70:
            return 'Fair'
        elif score >= 60:
            return 'Poor'
        else:
            return 'Critical'
    
    def get_behavior_recommendations(self, analysis):
        """Get recommendations based on behavior analysis"""
        recommendations = []
        
        for behavior, data in analysis.items():
            if data['concern_level'] != 'None':
                if behavior == 'eating' and data['status'] == 'Below Normal':
                    recommendations.extend([
                        'Check feed quality and availability',
                        'Examine cattle for dental issues',
                        'Consider veterinary consultation'
                    ])
                
                elif behavior == 'resting' and data['status'] == 'Above Normal':
                    recommendations.extend([
                        'Check for signs of illness',
                        'Ensure comfortable resting areas',
                        'Monitor temperature and vital signs'
                    ])
                
                elif behavior == 'walking' and data['status'] == 'Above Normal':
                    recommendations.extend([
                        'Check for environmental stressors',
                        'Ensure adequate shade and water',
                        'Monitor for heat stress symptoms'
                    ])
        
        # Remove duplicates
        recommendations = list(set(recommendations))
        
        if not recommendations:
            recommendations = ['Continue regular monitoring', 'Maintain current care routine']
        
        return recommendations
    
    def get_behavior_trends(self, cattle_id, days=7):
        """Get behavior trends over time"""
        trends = {}
        
        for behavior in self.behavior_patterns.keys():
            # Simulate trend data
            trend_data = []
            base_value = random.uniform(0.8, 1.2)
            
            for day in range(days):
                daily_variation = random.uniform(-0.1, 0.1)
                value = max(0.5, min(1.5, base_value + daily_variation))
                trend_data.append({
                    'date': (datetime.now() - timedelta(days=days-day-1)).strftime('%Y-%m-%d'),
                    'value': round(value, 2),
                    'status': 'Normal' if 0.8 <= value <= 1.2 else 'Abnormal'
                })
            
            trends[behavior] = trend_data
        
        return trends