import requests

# Login first
login_data = {"email": "test@test.com", "password": "test123"}
s = requests.Session()
r = s.post("http://localhost:5000/signup", json=login_data)
print("Signup:", r.json())

# Upload image
with open("dataset/Gir/Gir_1.jpg", "rb") as f:
    files = {"file": f}
    r = s.post("http://localhost:5000/predict", files=files)
    print("\nResponse:", r.status_code)
    print(r.json())
