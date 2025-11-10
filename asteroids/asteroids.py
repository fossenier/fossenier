import json
import os

from typing import List

# Speed calculator of platform
# https://www.desmos.com/calculator/eykhbatbn6
# https://www.desmos.com/calculator/a9ruvrbkvt

asteroid_size_health = {
    "medium": 745
}
asteroid_data = {
    "metallic-asteroid-chunk"
    "oxide-asteroid-chunk"
    "carbonic-asteroid-chunk"
    "medium-metallic-asteroid"
    "medium-oxide-asteroid"
    "medium-carbonic-asteroid"
}

class Asteroid:
    name: str

class Waypoint:
    distance: int
    asteroids: List[Asteroid]

class Route:
    path: str # file path to json data
    source: str # name of planet
    dest: str # name of planet
    
    def __init__(self) -> None:
        pass

def parse_route_file():
    

def main():
    # load in all json data
    planet_files: List[str] = []
    route_files: List[str] = []
    
    for file in os.listdir("./json"):
        if "_" in file:
            route_files.append(file)
        else:
            planet_files.append(file)
    
    for route_file in route_files:
        src_planet = route_file[0:route_file.find("_")]
        dest_planet = route_file[route_file.find("_") + 1:-5]
        
        with open("./json/" + src_planet + ".json", "r") as f:
            planet_data = json.load(f)
        
    
    gleba = [p for p in planet_files if "gleba" in p][0]
    
    with open("./json/" + gleba, 'r') as f:
        planet_data = json.load(f)

    origin_planet_rate_min = {}

    # Access the asteroid spawn definitions
    asteroid_spawn_definitions = planet_data["planet"]["asteroid_spawn_definitions"]
    print(asteroid_spawn_definitions[0])
    for asd in asteroid_spawn_definitions:
        origin_planet_rate_min[asd["asteroid"]] = asd["probability"] * 3600 # seconds in a minute
    
    print(origin_planet_rate_min)


# look at each route
# calculate base spawn rate (in each waypoint including linear planet effect)
# calculate total expected resources (asteroid chunks)
# see how much fuel could be used (max speed) on the least fuel rich route
# calculate how much damage at that speed
# calucalte all expected resources at that speed
# see what surplus is
# see how much science could be made
# find optimal platform size

# # Load the JSON file
# with open('./json/gleba.json', 'r') as f:
#     planet_data = json.load(f)

# # Access the asteroid spawn definitions
# asteroid_spawn_definitions = planet_data["planet"]["asteroid_spawn_definitions"]

# print(asteroid_spawn_definitions)

# with open('./json/gleba_fulgora.json', 'r') as f:
#     planet_data = json.load(f)

# asteroid_spawn_definitions = planet_data["space-connection"]["asteroid_spawn_definitions"]

# print(asteroid_spawn_definitions)

if __name__ == "__main__":
    main()