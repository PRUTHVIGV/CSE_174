import requests
import json

login_data = {"email": "test2@test.com", "password": "test123"}
s = requests.Session()
s.post("http://localhost:5000/signup", json=login_data)

with open("dataset/Gir/Gir_1.jpg", "rb") as f:
    files = {"file": f}
    r = s.post("http://localhost:5000/predict", files=files)
    data = r.json()
    print("Keys:", data.keys())
    if 'predictions' in data:
        print("First prediction keys:", data['predictions'][0].keys())
        print("Info keys:", data['predictions'][0]['info'].keys())
