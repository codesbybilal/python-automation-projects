import requests, json
response = requests.get(    "https://api.restcountries.com/countries/v5/names.common/Pakistan",
    headers={"Authorization": "Bearer rc_live_8fae51af2e624e0981fa8a87f448bfca"})
apiStatus = response.status_code
data = response.json()
print("Info about Pakistan")
print("Population: ",data["data"]["objects"][0]["population"])

print("Capital: ",data["data"]["objects"][0]["capitals"][0]["name"])

print("Currency: ",data["data"]["objects"][0]["currencies"][0]["name"])