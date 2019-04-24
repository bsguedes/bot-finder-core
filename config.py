PLAYERS = [
    ('127.0.0.1', 3000),
    ('127.0.0.1', 3001),
    ('127.0.0.1', 3002),
    ('127.0.0.1', 3003)
]

DIRS = {0: (1,  0),  1: (0,  1),  2: (-1,  0),  3: (0,  -1)}

SELECTED_MAP = 'default'

default_parameters = {
    'size': 900,
    'water_level': 5,
    'tree_level': 30,
    'reduction_rate': 90,
    'tree_percentage': 15,
    'rivers': 20,
    'river_level': 10,
    'landmarks': 100,
    'vision_radius': 4,
    'show_scores': True
}

small_parameters = {
    'size': 400,
    'water_level': 5,
    'tree_level': 30,
    'reduction_rate': 35,
    'tree_percentage': 15,
    'rivers': 20,
    'river_level': 10,
    'landmarks': 100,
    'vision_radius': 10,
    'show_scores': False
}

params = {
    'default': default_parameters,
    'small': small_parameters
}

SIZE = params[SELECTED_MAP]['size']
WATER_LEVEL = params[SELECTED_MAP]['water_level']
TREE_LEVEL = params[SELECTED_MAP]['tree_level']
REDUCTION_RATE = params[SELECTED_MAP]['reduction_rate']
TREE_PERCENTAGE = params[SELECTED_MAP]['tree_percentage']
RIVERS = params[SELECTED_MAP]['rivers']
RIVER_LEVEL = params[SELECTED_MAP]['river_level']
LANDMARKS = params[SELECTED_MAP]['landmarks']
VISION_RADIUS = params[SELECTED_MAP]['vision_radius']
SHOW_SCORES = params[SELECTED_MAP]['show_scores']

SEED = None
VERBOSE = False
RADIO_INTERVAL = 10
PLAYER_INTERVAL = 0.05
TOP_LEVEL = 100

