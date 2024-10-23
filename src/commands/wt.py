import network
from config import GameContext

NAME = 'wt'
DESCRIPTION = 'fetches last wt data'
CONTEXT = [GameContext.GAME]

def run():
    req = network.get_missions()
    print(req)