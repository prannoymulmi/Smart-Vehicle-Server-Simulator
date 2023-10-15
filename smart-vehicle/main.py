# post_request.py

import requests



url = 'https://localhost:5000/data'  # Replace with the URL you want to POST to

data = {
    'GPS': '12',
    'USER': 'test user'
}
response = requests.get('https://localhost:5000', verify=False)
print(response.text)
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers, verify=False)

print(f"Response Status Code: {response.status_code}")
print(f"Response Data: {response.text}")