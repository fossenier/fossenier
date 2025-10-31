import json
import os

json_files = os.listdir("./json")

planet_files = [f for f in json_files if "_" not in f]
route_files = [f for f in json_files if "_" in f]

# Print all files in ./json
json_files = os.listdir('./json')
print("All files in ./json:")
print(json_files)

# Print files in ./json that do not have "_" in the name
files_without_underscore = [f for f in json_files if '_' not in f]
print("Files in ./json without '_' in name:")
print(files_without_underscore)

# Load the JSON file
with open('./json/gleba.json', 'r') as f:
    planet_data = json.load(f)

# Access the asteroid spawn definitions
asteroid_spawn_definitions = planet_data["planet"]["asteroid_spawn_definitions"]

print(asteroid_spawn_definitions)

with open('./json/gleba_fulgora.json', 'r') as f:
    planet_data = json.load(f)

asteroid_spawn_definitions = planet_data["space-connection"]["asteroid_spawn_definitions"]

print(asteroid_spawn_definitions)