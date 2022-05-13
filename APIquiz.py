import json
import requests
import sqlite3

url = 'https://pokeapi.co/api/v2/pokemon'
resp = requests.get(url)

statusCode = resp.status_code
if statusCode == 200:
    print("Status: Success")
elif statusCode in [301, 302, 303]:
    print("Status: Redirection")
elif statusCode in [401, 403, 404, 405]:
    print("Status: Client Error")
elif statusCode in [501, 502, 503, 504]:
    print("Status: Server Error")
print(resp.headers['Content-Type'])

response_text = resp.text


resp_json = resp.json()
with open('PokeData.json', 'w') as file:
    json.dump(resp_json, file, indent=5)


with open('PokeData.json', 'r') as file:
    resp_json = json.load(file)
    user_pokemon = int(input("Choose Pokemon from 1 to 20: ")) - 1
    pokemon_resp = requests.get(resp_json['results'][user_pokemon]['url'])
    pokemon_resp_json = pokemon_resp.json()
    print(f"Pokemons Name: {pokemon_resp_json['name']} \n Height: {pokemon_resp_json['height']} \n Weight: {pokemon_resp_json['weight']}")
    
conn = sqlite3.connect('PokeData.sqlite')
cursor = conn.cursor()

# ვქმნი ბაზას სადაც ეწერება 20 პოკემონი და მათზე მონაცემი 
cursor.execute('''CREATE TABLE IF NOT EXISTS pokemons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(40),
                height INTEGER,
                weight INTEGER)''')
for i in range(20):
    pokemon_resp = requests.get(resp_json['results'][i]['url'])
    pokemon_resp_json = pokemon_resp.json()
    pokeinfo = (pokemon_resp_json['name'],pokemon_resp_json['height'], pokemon_resp_json['weight'] )
    cursor.execute("INSERT INTO pokemons (name, height, weight) VALUES (?, ?, ?)",pokeinfo)

conn.commit()
conn.close()