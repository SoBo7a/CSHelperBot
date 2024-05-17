import random

# List of available CS2 maps
cs2_maps = [
    "Dust II",
    "Mirage",
    "Inferno",
    "Nuke",
    "Overpass",
    "Vertigo",
    "Train",
    "Cache",
    "Cobblestone",
    "Ancient",
]

# List of available Wingman maps
wingman_maps = [
    "Assembly",
    "Boyard",
    "Chalice",
    "Cobblestone (B bombsite)",
    "Inferno (A bombsite)",
    "Lake",
    "Memento"
    "Overpass (B bombsite)",
    "Shortdust",
    "Shortnuke",
    "Train (A bombsite)",
    "Vertigo (B bombsite)",
]

# Function to get a random map from a given list
def get_random_map(maps):
    return random.choice(maps)