import requests
response = requests.get("https://api.github.com/users/codesbybilal")
if response.status_code == 200:
    data = response.json()
    print(response.status_code)
    print("Github Info of @codesbybilal")
    print("Name: ", data["name"])
    print("Bio: ", data["bio"])
    print("Followers: ", data["followers"])
elif response.status_code == 404:
    print("User not found.")
else:
    print(f"Something went wrong. Error {response.status_code}")
