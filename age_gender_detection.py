import cv2
import numpy as np
import random

class CattleAttributeDetector:
    def __init__(self):
        self.age_ranges = {
            'calf': (0, 12),
            'young': (12, 24), 
            'adult': (24, 72),
            'senior': (72, 120)
        }
        
    def detect_age_gender(self, image_path):
        """Detect age and gender from cattle image"""
        # Simulate age detection based on visual features
        age_months = random.randint(6, 96)
        gender = random.choice(['Male', 'Female'])
        
        # Determine age category
        age_category = 'adult'
        for category, (min_age, max_age) in self.age_ranges.items():
            if min_age <= age_months < max_age:
                age_category = category
                break
        
        # Simulate confidence based on image quality
        age_confidence = random.uniform(0.75, 0.95)
        gender_confidence = random.uniform(0.80, 0.96)
        
        return {
            'age_months': age_months,
            'age_category': age_category,
            'age_confidence': age_confidence,
            'gender': gender,
            'gender_confidence': gender_confidence,
            'breeding_status': self.assess_breeding_status(age_months, gender),
            'market_value': self.estimate_market_value(age_months, gender)
        }
    
    def assess_breeding_status(self, age_months, gender):
        """Assess breeding readiness"""
        if gender == 'Female':
            if age_months >= 18:
                return 'Breeding Ready'
            elif age_months >= 12:
                return 'Pre-breeding'
            else:
                return 'Too Young'
        else:  # Male
            if age_months >= 24:
                return 'Breeding Bull'
            elif age_months >= 18:
                return 'Young Bull'
            else:
                return 'Too Young'
    
    def estimate_market_value(self, age_months, gender):
        """Estimate market value based on age and gender"""
        base_value = 50000  # Base price in INR
        
        # Age factor
        if age_months < 12:
            age_factor = 0.4
        elif age_months < 24:
            age_factor = 0.7
        elif age_months < 60:
            age_factor = 1.0
        else:
            age_factor = 0.8
        
        # Gender factor
        gender_factor = 1.2 if gender == 'Female' else 1.0
        
        estimated_value = int(base_value * age_factor * gender_factor)
        return f"₹{estimated_value:,}"