import requests
# URL that the server is on 
BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "game/1")
print(response.json())

response = requests.get(BASE + "game/2")
print(response.json())

response = requests.put(BASE + "game/3?name=Tetris&users=300&likes=500")
print(response.json())

response = requests.delete(BASE + "game/3")
print(response)

response = requests.get(BASE + "game/3")
print(response.json())