# bot-finder-core

## To install the core

After cloning the repository:

You're going to need Python3.5 at least (on Ubuntu 18, this shouldn't be necessary, since it has Python 3.6 already).

### If you need Python 3.5 (Ubuntu 14)

Follow the steps on https://tecadmin.net/install-python-3-5-on-ubuntu/

If you did the steps above, install the project requirements with `sudo pip3.5 install -r requirements.txt`. 

If tkinter is not installed, install it with `sudo apt-get install python3.5-tk`.

Run the game: `python3 main.py`

### If you already have Python 3.6 (Ubuntu 18)

Install `pip` if it is not installed yet: `sudo apt-get install python3-pip` 

Run `pip3 install -r requirements.txt`.

Install tkinter: `sudo apt-get install python3.6-tk`

Run the game: `python3 main.py`

## Goal

The game sets multiple bots into an island. These bots have limited vision, they can only see a few steps around them.

They get information about the terrain in the surroundings (water, trees, land) and they can notice unique landmarks in the island.

The goal is to gather all bots into a same location, based on this really limited information.

## Landmarks

To help bots to locate each other, the island has some landmarks that have a unique ID. It is wise to keep track of all landmarks found: if one or more bots have found the same landmarks, they can evaluate their relative positions and then meet with each other!

## Radio

Every few seconds, bots can post a radio message that is broadcast to all other bots. It is the only way that bots can communicate with each other on this island.

## API details

Each bot has to expose a REST API with the following endpoints:

### GET /players/name

Expects a JSON (application/json) containing the name of the player. Every time this is called, a new game begins.

It is expected that the API returns this payload:

```
{ 'name': 'bot_name' } 
```

Please keep the name down to 8 characters.

### PUT /players/:player_name/move

The game sends this payload in this call:

```
{ 'vision': (VisionObject) }
```

Where `VisionObject` is an integer 2D array, indexed first by `x` then by `y`, containing what the bot currently sees. **Your player will always be in the center of the square**. Each field has these possible values:

```
-1: darkness (your sight does not reach the corners of the square)
0: land (walkable terrain)
1: water (rivers and sea; impassable terrain) 
2: tree (only on land; impassable)
100..999 (a landmark; each landmark is unique and impassable)
1000, 1001, 1002, ... 1000 + x (a player, where x is the player ID) 
```

There is also a custom header, `Valid-Last-Move`, which contains a boolean value informing if the last move the player executed was valid or not.

The expected return value from the bots is one of the four possible directions in this format:

```
{ 'direction': ('north', 'south', 'east', 'west') }
```

### GET /players/:player_name/radio

Expects a JSON (application/json) containing data that will be sent to all players, under a `radio` key.

It is expected that the API returns this payload:

```
{ 'radio': (RadioObject) } 
```

Where `RadioObject` is a JSON object with whatever data you wish.

### POST /players/:player_name/radio

The API posts to each player through this route the contents of every radio signal with the following payload:

```
{ 'player_1': (RadioObject), 'player_2': (RadioObject), ... } 
```

All radio messages are broadcast to all players (including the message you sent before)

Radio messages are not necessarily synced. 

## Example

An very simple example of a bot can be found in my bot-finder-player repository on GitHub.

## To run a server at internal network

Start a server disabling proxy and binding it to 0.0.0.0:

```
unset http_proxy; unset HTTP_PROXY; rails s --binding 0.0.0.0
```
