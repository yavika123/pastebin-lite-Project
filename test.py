import requests

# Data for new paste
data = {
    "content": "Hello World",
    "ttl_seconds": 3600,
    "max_views": 2
}

# Send POST request
response = requests.post("http://127.0.0.1:5000/api/pastes", json=data)

# Show the response
print(response.json())
