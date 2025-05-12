import json
import os

import network
from config import GameContext

NAME = "wt"
DESCRIPTION = "fetches last wt data"
CONTEXT = [GameContext.GAME]


def format_player(player):
    formatted = {}

    formatted["id"] = player["id"]
    formatted["rank"] = player["ranking"]
    formatted["points"] = player["point"]
    formatted["win_count"] = player["title_num"]
    formatted["continuous_win_count"] = player["continuous_title_num_max"]
    formatted["name"] = player["name"]

    # rarity and element are 100% made up but we won't use it so it's fine
    formatted["leader_card_id"] = {
        "id": player["leader"]["id"],
        "rarity": 0,
        "element": 0,
    }

    return formatted


def format_json(original):
    formatted = {}
    formatted["pagination"] = {
        "current_page": original["current_page"],
        "total_pages": original["total_page"],
    }

    # You'll update them both anyway or maybe you won't even go that far but I need them for compatibility reasons
    formatted["rank1000_updated_at"] = original["updated_at"]
    formatted["rank10000_updated_at"] = original["updated_at"]

    formatted["players"] = [format_player(i) for i in original["rankers"]]

    return formatted


def merge_pages(page_1, page_2):
    if page_1:
        page_1["players"] += page_2["players"]
        return page_1
    else:
        return page_2


def run(n: int = 100, budokai_id: int = 1):
    n_page = int(int(n) / 100)
    file = {}
    for i in range(1, n_page + 1):
        data = network.get_budokai_rankings(budokai_id=budokai_id, page=i)
        file = merge_pages(file, format_json(data))
    return file
