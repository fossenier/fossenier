import json
import os

from typing import Dict, List, Set, Tuple

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

class Planet:
    rates: List[Tuple[str, float]] # asteroid per second at planet

class Waypoint:
    distance: float # % of the way from source to dest for route
    rates: Set[Tuple[str, float]] # asteroid per second at distance

    def __init__(self, distance: float):
        self.distance = distance
        self.rates = set()

    def add_rate(self, asteroid: str, rate: float):
        self.rates.add((asteroid, rate))

    def __str__(self) -> str:
        output = ""
        output += "Waypoint\n"
        output += f"distance: {self.distance}\n"
        output += f"asteroid spawn rates (asteroids per second):\n"
        # alphabetical by asteroid name
        for rate in sorted(self.rates, key=lambda entry: entry[0]):
            output += f"   {rate[0]}{" " * (29 - len(rate[0]))}  {rate[1]:.6f}\n"
        
        return output


class Route:
    path: str # file path to json data
    source: Planet # name of planet
    dest: Planet # name of planet
    waypoints: Dict[float, "Waypoint"] # from source to dest, invert as needed

    def __init__(self, path: str, source: Planet, dest: Planet) -> None:
        self.path = path
        self.source = source
        self.dest = dest
        self.waypoints = dict()

        # read in waypoint data
        with open("./json/" + self.path, "r") as f:
            data = json.load(f)
            spawn_defs = data["space-connection"]["asteroid_spawn_definitions"]
            for sd in spawn_defs:
                name = sd["asteroid"]
                for point in sd["spawn_points"]:
                    distance = point["distance"]
                    probability = point["probability"]
                    # grab the right waypoint or create it
                    try:
                        waypoint = self.waypoints[distance]
                    except KeyError:
                        waypoint = Waypoint(distance)
                        self.waypoints[distance] = waypoint
                    # add a rate for this asteroid to the corresponding waypoint
                    waypoint.add_rate(name, probability)

        for w in self.waypoints.values():
            print(w)


def parse_route_file():
    pass
    

def main():
    # load in all json data
    planet_files: List[str] = []
    route_files: List[str] = []
    
    for file in os.listdir("./json"):
        print(file)
        if "_" in file:
            route_files.append(file)
        else:
            planet_files.append(file)
    
    
    for route_file in route_files:
        route = Route(route_file, Planet(), Planet())
        return
        src_planet = route_file[0:route_file.find("_")]
        dest_planet = route_file[route_file.find("_") + 1:-5]
        
        with open("./json/" + src_planet + ".json", "r") as f:
            planet_data = json.load(f)
        
    
    gleba = [p for p in planet_files if "nauvis" in p][0]
    
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