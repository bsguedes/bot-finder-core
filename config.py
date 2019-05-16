PLAYERS = [
    ('127.0.0.1', 3000),
    ('127.0.0.1', 3001),
    ('127.0.0.1', 3002),
    ('127.0.0.1', 3003),
    ('127.0.0.1', 3004),
]

DIRS = {0: (1,  0),  1: (0,  1),  2: (-1,  0),  3: (0,  -1)}

SELECTED_MAP = 'small'

default_parameters = {
    'size_x': 900,
    'size_y': 900,
    'island_lower_level': 2,
    'island_top_level': 3,
    'water_level': 5,
    'tree_level': 30,
    'reduction_rate': 85,
    'tree_percentage': 15,
    'rivers': 20,
    'river_level': 10,
    'landmarks': 100,
    'vision_radius': 4,
    'show_scores': True,
    'zoom': 1
}

large_parameters = {
    'size_x': 1500,
    'size_y': 1000,
    'island_lower_level': 0.15,
    'island_top_level': 0.2,
    'water_level': 0.25,
    'tree_level': 8,
    'reduction_rate': 99,
    'tree_percentage': 10,
    'rivers': 20,
    'river_level': 1,
    'landmarks': 100,
    'vision_radius': 4,
    'show_scores': True,
    'zoom': 1
}

small_parameters = {
    'size_x': 400,
    'size_y': 400,
    'island_lower_level': 2,
    'island_top_level': 3,
    'water_level': 5,
    'tree_level': 30,
    'reduction_rate': 35,
    'tree_percentage': 15,
    'rivers': 20,
    'river_level': 10,
    'landmarks': 100,
    'vision_radius': 10,
    'show_scores': False,
    'zoom': 2
}

tiny_parameters = {
    'size_x': 250,
    'size_y': 250,
    'island_lower_level': 2,
    'island_top_level': 3,
    'water_level': 5,
    'tree_level': 30,
    'reduction_rate': 20,
    'tree_percentage': 5,
    'rivers': 5,
    'river_level': 10,
    'landmarks': 20,
    'vision_radius': 10,
    'show_scores': False,
    'zoom': 4
}

params = {
    'default': default_parameters,
    'small': small_parameters,
    'large': large_parameters,
    'tiny': tiny_parameters
}

SIZE_X = params[SELECTED_MAP]['size_x']
SIZE_Y = params[SELECTED_MAP]['size_y']
WATER_LEVEL = params[SELECTED_MAP]['water_level']
TREE_LEVEL = params[SELECTED_MAP]['tree_level']
REDUCTION_RATE = params[SELECTED_MAP]['reduction_rate']
TREE_PERCENTAGE = params[SELECTED_MAP]['tree_percentage']
RIVERS = params[SELECTED_MAP]['rivers']
RIVER_LEVEL = params[SELECTED_MAP]['river_level']
LANDMARKS = params[SELECTED_MAP]['landmarks']
VISION_RADIUS = params[SELECTED_MAP]['vision_radius']
SHOW_SCORES = params[SELECTED_MAP]['show_scores']
ISLAND_TOP_LEVEL = params[SELECTED_MAP]['island_top_level']
ISLAND_LOWER_LEVEL = params[SELECTED_MAP]['island_lower_level']
ZOOM = params[SELECTED_MAP]['zoom']

SEED = None
VERBOSE = False
RADIO_INTERVAL = 10
PLAYER_INTERVAL = 0.05
TOP_LEVEL = 100
