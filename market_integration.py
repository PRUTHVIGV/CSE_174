import random
from datetime import datetime, timedelta

class MarketPriceIntegration:
    def __init__(self):
        # Base prices in INR per cattle
        self.base_prices = {
            'Gir': 80000,
            'Sahiwal': 75000,
            'Red_Sindhi': 65000,
            'Tharparkar': 60000,
            'Ongole': 70000,
            'Hariana': 55000,
            'Kankrej': 65000,
            'Rathi': 50000,
            'Murrah_Buffalo': 90000,
            'Mehsana_Buffalo': 75000
        }
        
        self.market_locations = {
            'Gujarat': 1.1,
            'Punjab': 1.05,
            'Haryana': 1.08,
            'Rajasthan': 0.95,
            'Maharashtra': 1.02,
            'Uttar_Pradesh': 0.98
        }
    
    def get_current_price(self, breed, location='Gujarat', age_months=24, gender='Female'):
        """Get current market price for cattle"""
        base_price = self.base_prices.get(breed, 60000)
        location_factor = self.market_locations.get(location, 1.0)
        
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
        
        # Market fluctuation
        market_fluctuation = random.uniform(0.9, 1.1)
        
        current_price = int(base_price * location_factor * age_factor * gender_factor * market_fluctuation)
        
        return {
            'current_price': f"₹{current_price:,}",
            'price_range': f"₹{int(current_price*0.9):,} - ₹{int(current_price*1.1):,}",
            'market_trend': self.get_market_trend(),
            'price_factors': {
                'base_price': f"₹{base_price:,}",
                'location_factor': f"{location_factor:.2f}x",
                'age_factor': f"{age_factor:.2f}x",
                'gender_factor': f"{gender_factor:.2f}x"
            },
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    
    def get_market_trend(self):
        """Get market trend analysis"""
        trends = ['Rising', 'Stable', 'Declining']
        trend = random.choice(trends)
        
        trend_data = {
            'Rising': {'direction': '📈', 'change': '+5-8%', 'recommendation': 'Good time to sell'},
            'Stable': {'direction': '➡️', 'change': '±2%', 'recommendation': 'Market is steady'},
            'Declining': {'direction': '📉', 'change': '-3-5%', 'recommendation': 'Consider holding'}
        }
        
        return {
            'trend': trend,
            'direction': trend_data[trend]['direction'],
            'change': trend_data[trend]['change'],
            'recommendation': trend_data[trend]['recommendation']
        }
    
    def get_price_history(self, breed, days=30):
        """Get price history for breed"""
        base_price = self.base_prices.get(breed, 60000)
        history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            fluctuation = random.uniform(0.85, 1.15)
            price = int(base_price * fluctuation)
            
            history.append({
                'date': date.strftime("%Y-%m-%d"),
                'price': price,
                'formatted_price': f"₹{price:,}"
            })
        
        return history
    
    def compare_breeds(self, location='Gujarat'):
        """Compare prices across breeds"""
        comparison = []
        
        for breed, base_price in self.base_prices.items():
            location_factor = self.market_locations.get(location, 1.0)
            market_price = int(base_price * location_factor * random.uniform(0.9, 1.1))
            
            comparison.append({
                'breed': breed,
                'price': market_price,
                'formatted_price': f"₹{market_price:,}",
                'category': 'Buffalo' if 'Buffalo' in breed else 'Cattle'
            })
        
        # Sort by price
        comparison.sort(key=lambda x: x['price'], reverse=True)
        return comparison
    
    def get_investment_analysis(self, breed, initial_investment, years=3):
        """Get investment analysis for cattle farming"""
        base_price = self.base_prices.get(breed, 60000)
        
        # Annual returns (milk, breeding, etc.)
        annual_returns = {
            'Gir': 25000,
            'Sahiwal': 22000,
            'Murrah_Buffalo': 35000,
            'Mehsana_Buffalo': 28000
        }
        
        annual_return = annual_returns.get(breed, 20000)
        total_returns = annual_return * years
        
        # Appreciation in cattle value
        appreciation_rate = 0.08  # 8% per year
        final_value = int(initial_investment * (1 + appreciation_rate) ** years)
        
        total_profit = total_returns + final_value - initial_investment
        roi = (total_profit / initial_investment) * 100
        
        return {
            'initial_investment': f"₹{initial_investment:,}",
            'annual_returns': f"₹{annual_return:,}",
            'total_returns': f"₹{total_returns:,}",
            'final_cattle_value': f"₹{final_value:,}",
            'total_profit': f"₹{total_profit:,}",
            'roi_percentage': f"{roi:.1f}%",
            'payback_period': f"{initial_investment/annual_return:.1f} years"
        }