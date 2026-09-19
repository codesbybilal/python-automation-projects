import requests
response = requests.get("https://api.github.com/users/codesbybilal")
data = response.json()
print("Github Info of @codesbybilal")
print("Name: ", data["name"])
print("Bio: ", data["bio"])
print("Followers: ", data["followers"])