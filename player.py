import config
import requests
from requests.exceptions import RequestException


class Player:    
    def __init__(self, name, pid, x, y, ip, port):
        self.player_id = pid - 1
        self.x = x
        self.y = y
        self.ip = ip
        self.port = port
        self.vision = None
        self.steps = 0
        self.name = self.obtain_name(name)

    def obtain_name(self, default_name):
        try:
            r = requests.get('http://%s:%s/player/name' % (self.ip, self.port))
            return r.content['name']
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            return default_name

    def move(self, vision):
        self.vision = vision
        try:
            r = requests.put('http://%s:%s/player/move' % (self.ip, self.port), data=payload(vision))
            direction = parse_response(r.content['direction'])
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            direction = -1
        self.steps += 1
        return direction

    def obtain_radio(self):
        try:
            r = requests.get('http://%s:%s/player/radio' % (self.ip, self.port))
            return r.content['radio']
        except RequestException as e:
            if config.VERBOSE:
                print(e)
            return ''

    def post_radio(self, radio_stream):
        try:
            requests.post('http://%s:%s/player/radio' % (self.ip, self.port), data=radio_stream)
        except RequestException as e:
            if config.VERBOSE:
                print(e)

    def update_position(self, direction):
        if direction >= 0:
            self.x += config.DIRS[direction][0]
            self.y += config.DIRS[direction][1]


def payload(vision):
    return {
        'vision': vision
    }


def parse_response(content):
    if content == 'east':
        return 0
    elif content == 'north':
        return 1
    elif content == 'west':
        return 2
    elif content == 'south':
        return 3
    return -1
