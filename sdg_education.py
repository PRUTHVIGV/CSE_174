import random
from datetime import datetime

class EducationModule:
    def __init__(self):
        self.courses = {
            'basic_cattle_care': {
                'title': 'Basic Cattle Care & Management',
                'duration': '2 weeks',
                'modules': ['Feeding', 'Housing', 'Health Care', 'Breeding'],
                'language': ['Hindi', 'English', 'Gujarati'],
                'difficulty': 'Beginner'
            },
            'breed_identification': {
                'title': 'Indian Cattle Breed Identification',
                'duration': '1 week',
                'modules': ['Breed Characteristics', 'Visual Recognition', 'Economic Importance'],
                'language': ['Hindi', 'English'],
                'difficulty': 'Intermediate'
            },
            'modern_farming': {
                'title': 'Modern Dairy Farming Techniques',
                'duration': '3 weeks',
                'modules': ['Technology Integration', 'AI in Farming', 'Market Analysis'],
                'language': ['English', 'Hindi'],
                'difficulty': 'Advanced'
            },
            'financial_literacy': {
                'title': 'Financial Management for Farmers',
                'duration': '2 weeks',
                'modules': ['Budgeting', 'Loans', 'Insurance', 'Market Trading'],
                'language': ['Hindi', 'English', 'Regional'],
                'difficulty': 'Intermediate'
            }
        }
        
        self.learning_paths = {
            'new_farmer': ['basic_cattle_care', 'breed_identification', 'financial_literacy'],
            'experienced_farmer': ['modern_farming', 'breed_identification'],
            'student': ['breed_identification', 'basic_cattle_care', 'modern_farming'],
            'entrepreneur': ['financial_literacy', 'modern_farming', 'breed_identification']
        }
    
    def get_personalized_learning_path(self, user_profile):
        """Generate personalized learning path based on user profile"""
        experience = user_profile.get('experience', 'new')
        role = user_profile.get('role', 'farmer')
        language = user_profile.get('language', 'Hindi')
        
        # Determine user category
        if role == 'student':
            category = 'student'
        elif role == 'entrepreneur':
            category = 'entrepreneur'
        elif experience in ['beginner', 'new']:
            category = 'new_farmer'
        else:
            category = 'experienced_farmer'
        
        recommended_courses = self.learning_paths.get(category, self.learning_paths['new_farmer'])
        
        learning_plan = []
        for course_id in recommended_courses:
            course = self.courses[course_id].copy()
            course['id'] = course_id
            course['available_in_language'] = language in course['language']
            learning_plan.append(course)
        
        return {
            'user_category': category,
            'recommended_courses': learning_plan,
            'total_duration': self.calculate_total_duration(recommended_courses),
            'sdg_alignment': 'SDG-04: Quality Education for Sustainable Agriculture'
        }
    
    def calculate_total_duration(self, course_ids):
        """Calculate total learning duration"""
        total_weeks = 0
        for course_id in course_ids:
            duration_str = self.courses[course_id]['duration']
            weeks = int(duration_str.split()[0])
            total_weeks += weeks
        return f"{total_weeks} weeks"
    
    def get_interactive_lesson(self, course_id, module_name):
        """Get interactive lesson content"""
        lessons = {
            'breed_identification': {
                'Visual Recognition': {
                    'content': 'Learn to identify cattle breeds by visual characteristics',
                    'quiz': [
                        {'question': 'Which breed is known for high milk yield?', 'options': ['Gir', 'Ongole', 'Kankrej'], 'answer': 'Gir'},
                        {'question': 'Murrah is a breed of?', 'options': ['Cattle', 'Buffalo', 'Goat'], 'answer': 'Buffalo'}
                    ],
                    'practical': 'Use AI tool to identify 5 different cattle images'
                }
            },
            'basic_cattle_care': {
                'Feeding': {
                    'content': 'Proper nutrition is essential for cattle health and productivity',
                    'quiz': [
                        {'question': 'How much water does a dairy cow need daily?', 'options': ['20L', '50L', '100L'], 'answer': '50L'}
                    ],
                    'practical': 'Calculate feed requirements for your cattle'
                }
            }
        }
        
        return lessons.get(course_id, {}).get(module_name, {
            'content': f'Interactive lesson for {module_name}',
            'quiz': [],
            'practical': 'Hands-on activity'
        })
    
    def generate_certificate(self, user_name, course_id, score):
        """Generate digital certificate"""
        course = self.courses.get(course_id, {})
        
        return {
            'certificate_id': f"CATTLE-EDU-{random.randint(10000, 99999)}",
            'user_name': user_name,
            'course_title': course.get('title', 'Cattle Management Course'),
            'completion_date': datetime.now().strftime('%Y-%m-%d'),
            'score': f"{score}%",
            'grade': 'A' if score >= 90 else 'B' if score >= 80 else 'C',
            'sdg_contribution': 'Contributing to SDG-04: Quality Education',
            'blockchain_verified': True,
            'skills_acquired': course.get('modules', [])
        }
    
    def get_farmer_network(self, location):
        """Connect farmers for peer learning"""
        return {
            'local_farmers': random.randint(50, 200),
            'expert_mentors': random.randint(5, 15),
            'study_groups': random.randint(3, 10),
            'upcoming_workshops': [
                {'title': 'AI in Cattle Farming', 'date': '2024-02-15', 'location': location},
                {'title': 'Breed Selection Workshop', 'date': '2024-02-22', 'location': location}
            ],
            'success_stories': [
                {'farmer': 'Ramesh Kumar', 'achievement': 'Increased milk yield by 30% using AI recommendations'},
                {'farmer': 'Priya Sharma', 'achievement': 'Reduced cattle mortality by 50% through better care'}
            ]
        }