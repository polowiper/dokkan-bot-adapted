import network
from config import GameContext
import os
import json
NAME = 'wt'
DESCRIPTION = 'fetches last wt data'
CONTEXT = [GameContext.GAME]

#caca 1 2 3 

def run():
    print("What pahe do you want ?")
    page = input()
    print("What wt do you want ?")
    budokai_id = input()
    data = network.get_budokai_rankings(budokai_id=budokai_id, page=page)
    with open(f"wt{budokai_id}.{page}.json", "w") as f:
        json.dump(data, f)

    