INDIAN_BREEDS = {
    "Gir": {"name": "Gir", "hindi": "गिर", "origin": "Gir Forest, Gujarat", "type": "Dairy", 
            "milk_yield": "10-12 L/day", "special": "World-famous dairy breed, exported globally"},
    "Sahiwal": {"name": "Sahiwal", "hindi": "साहीवाल", "origin": "Punjab", "type": "Dairy",
                "milk_yield": "8-10 L/day", "special": "Best heat-tolerant dairy breed"},
    "Red_Sindhi": {"name": "Red Sindhi", "hindi": "लाल सिंधी", "origin": "Sindh region", "type": "Dairy",
                   "milk_yield": "6-8 L/day", "special": "Excellent for crossbreeding programs"},
    "Tharparkar": {"name": "Tharparkar", "hindi": "थारपारकर", "origin": "Tharparkar, Rajasthan", "type": "Dual Purpose",
                   "milk_yield": "4-6 L/day", "special": "Excellent desert adaptation"},
    "Ongole": {"name": "Ongole", "hindi": "ओंगोल", "origin": "Ongole, Andhra Pradesh", "type": "Draught",
               "milk_yield": "3-5 L/day", "special": "Parent of American Brahman cattle"},
    "Hariana": {"name": "Hariana", "hindi": "हरियाणा", "origin": "Haryana", "type": "Dual Purpose",
                "milk_yield": "6-8 L/day", "special": "Versatile dual-purpose breed"},
    "Kankrej": {"name": "Kankrej", "hindi": "कांकरेज", "origin": "Gujarat-Rajasthan border", "type": "Draught",
                "milk_yield": "4-6 L/day", "special": "Most powerful draught breed"},
    "Rathi": {"name": "Rathi", "hindi": "राठी", "origin": "Bikaner, Rajasthan", "type": "Dairy",
              "milk_yield": "5-7 L/day", "special": "Best dairy breed for desert regions"},
    "Murrah_Buffalo": {"name": "Murrah Buffalo", "hindi": "मुर्रा भैंस", "origin": "Haryana", "type": "Dairy",
                       "milk_yield": "12-18 L/day", "special": "World's best dairy buffalo"},
    "Mehsana_Buffalo": {"name": "Mehsana Buffalo", "hindi": "मेहसाणा भैंस", "origin": "Mehsana, Gujarat", "type": "Dairy",
                        "milk_yield": "8-12 L/day", "special": "Cross between Murrah and Surti"}
}

def get_breed_info(breed_name):
    return INDIAN_BREEDS.get(breed_name, {})

def get_all_breeds():
    return list(INDIAN_BREEDS.keys())
