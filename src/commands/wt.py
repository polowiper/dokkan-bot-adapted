import network
from config import GameContext
import os
import json
NAME = 'wt'
DESCRIPTION = 'fetches last wt data'
CONTEXT = [GameContext.GAME]

def count_budokai_rankings(budokai_id):
    # Initialize a dictionary to store counts for each budokai_rank from 12 to 6
    counts = {12: 0, 11: 0, 10: 0, 9: 0, 8: 0, 7: 0, 6: 0}
    
    # Fetch the first page to get total number of pages
    response = network.get_budokai_rankings(budokai_id=budokai_id, page=1)
    total_pages = response['total_page']
    per_page = response['per_page']  # Number of players per page (always 100)
    
    # Set the current page
    current_page = 1

    while current_page <= total_pages:
        # Fetch current page of rankings
        print(counts)
        response = network.get_budokai_rankings(budokai_id=budokai_id, page=current_page)
        rankers = response["rankers"]
        
        # Get the budokai_rank for the first and last player on the page
        first_ranking = rankers[0]["budokai_rank"]
        last_ranking = rankers[-1]["budokai_rank"]

        if first_ranking == last_ranking:
            # If all players on this page have the same budokai_rank, add the length of the rankers list
            if 6 <= first_ranking <= 12:
                counts[first_ranking] += len(rankers)
        else:
            # Otherwise, count each player individually
            for player in rankers:
                ranking = player["budokai_rank"]
                if 6 <= ranking <= 12:
                    counts[ranking] += 1
        
        # Stop if the lowest rank on the page is less than 6
        if last_ranking < 6:
            break

        # Move to the next page
        current_page += 1

    return counts


def run():
    print("What pahe do you want ?")
    page = input()
    print("What wt do you want ?")
    budokai_id = input()
    print("Do you want to get all the data out of it ?")
    all = input()
    if all == "yes":
        count = count_budokai_rankings(budokai_id)
        print(count)
    else:
        data = network.get_budokai_rankings(budokai_id=budokai_id, page=page)
        with open(f"wt{budokai_id}.{page}.json", "w") as f:
            json.dump(data, f)

    