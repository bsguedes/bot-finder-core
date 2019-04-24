import config
import requests
from requests.exceptions import RequestException


class Player:    
    def __init__(self, name, pid, x, y, ip, port):
        self.player_id = pid - 1
        self.x = x
        self.y = y
        self.base_url = 'http://%s:%s' % (ip, port)
        self.vision = None
        self.steps = 0
        self.name = self.obtain_name(name)
        self.last_move_valid = None

    def obtain_name(self, default_name):
        try:
            r = requests.get('%s/players/name' % self.base_url)
            return r.json()['name']
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            return default_name

    def move(self, vision):
        self.vision = vision
        try:
            r = requests.put('%s/players/%s/move' % (self.base_url, self.name), json=payload(vision),
                             headers={'Valid-Last-Move': str(self.last_move_valid)})
            direction = parse_response(r.json()['direction'])
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            direction = -1
        self.steps += 1
        return direction

    def obtain_radio(self):
        try:
            r = requests.get('%s/players/%s/radio' % (self.base_url, self.name))
            return r.json()['radio']
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            return ''

    def post_radio(self, radio_stream):
        try:
            requests.post('%s/players/%s/radio' % (self.base_url, self.name), json=radio_stream)
        except RequestException as e:
            if config.VERBOSE:
                print(e)

    def update_position(self, direction, valid_move):
        if direction >= 0 and valid_move:
            self.x += config.DIRS[direction][0]
            self.y += config.DIRS[direction][1]
        self.last_move_valid = valid_move


def payload(vision):
    return {
        'vision': vision
    }


def parse_response(content):
    content = content.lower()
    if content == 'east':
        return 0
    elif content == 'north':
        return 1
    elif content == 'west':
        return 2
    elif content == 'south':
        return 3
    return -1
