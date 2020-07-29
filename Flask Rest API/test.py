import requests
# URL that the server is on 
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "game/2")
print(response.json())