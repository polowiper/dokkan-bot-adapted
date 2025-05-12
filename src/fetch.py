"""
TO SETUP THE ACCOUNT VARIABLE YOU WILL NEED TO MAKE AN ACCOUNT

FOR THAT PLEASE RUN THE main.py FILE AND MAKE A NEW ACCOUNT WITH IT

THE ACCOUNT VARIABLE SHOULD BE THE ACCOUNT'S NAME AS THE SAVES ARE SAVED AS:
saves/{acc name}.json
"""

import json
import os
import time

import requests
from colorama import Fore, init

import cli
import config
from classes.Game import GameEnvironment
from commands import load, wt
from services.command import CommandService

ACCOUNT = "polo"  # example
FETCH_SZ = 1000  # Keep in mind that we have to fetch 1 page every 100 people so the larger it is the longer it will take
WT_EDITION = 58
DELAY = 15  # The delay between each fetch (in minutes) I recomment something under 15 mins but not too small either to avoid problems something like 5 or 7 should do the trick I guess
SAVE_PATH = "fetches"  # You can change that to send the fetches to a specific place directly (for example in your local copy of Ludicolo :kek:)
LATEST_FETCH = 0  # After consideration this should prob be moved to another place like a json file to be able to give it it's latest value in case the file crashes but it will do the trick

init(autoreset=True)


# before anything a request for new URL & API port is required. - k1mpl0s
def check_servers(env: GameEnvironment):
    print("Checking servers...")
    try:
        url = env.url + "/ping"
        # we send an ancient version code that is valid.
        headers = {
            "X-Platform": "android",
            "X-ClientVersion": env.version_code,
            "X-Language": "en",
            "X-UserID": "////",
        }
        r = requests.get(url, data=None, headers=headers)
        # store our requested data into a variable as json.
        store = r.json()
        if "error" in store:
            print(Fore.RED + "[" + env.name + " server] " + str(store["error"]))
            return False
    except:
        print(Fore.RED + "[" + env.name + " server] can't connect.")
        return False
    return True


if check_servers(config.game_env):

    while True:
        load.run(ACCOUNT)

        if os.path.exists(f"{SAVE_PATH}/{LATEST_FETCH-1}.json"):
            ping = wt.run(100, WT_EDITION)
            with open(f"{SAVE_PATH}/{LATEST_FETCH-1}.json", "r") as f:
                prev_data = json.load(f)

            if (
                ping["rank1000_updated_at"] != prev_data["rank1000_updated_at"]
            ):  # "If it has changed then we fetch": Confiucus

                fetch = wt.run(FETCH_SZ, WT_EDITION)

                with open(os.path.join(SAVE_PATH, f"{LATEST_FETCH}.json"), "w") as e:
                    json.dump(fetch, e, indent=3)
                LATEST_FETCH += 1

        else:  # That means first fetch so we just fetch it
            fetch = wt.run(FETCH_SZ, WT_EDITION)
            with open(os.path.join(SAVE_PATH, f"{LATEST_FETCH}.json"), "w") as e:
                json.dump(fetch, e, indent=3)
            LATEST_FETCH += 1
        time.sleep(60 * DELAY)

else:
    print(Fore.RED + "press ENTER to close...")
    input()
    exit()
