import argparse
import json
import os
import time

import requests
from colorama import Fore, init

import config
from classes.Game import GameEnvironment
from commands import load_fetch, wt

LATEST_FETCH = 0

init(autoreset=True)


def check_servers(env: GameEnvironment):
    print("Checking servers...")
    try:
        url = env.url + "/ping"
        headers = {
            "X-Platform": "android",
            "X-ClientVersion": env.version_code,
            "X-Language": "en",
            "X-UserID": "////",
        }
        r = requests.get(url, data=None, headers=headers)
        store = r.json()
        if "error" in store:
            print(Fore.RED + "[" + env.name + " server] " + str(store["error"]))
            return False
    except:
        print(Fore.RED + "[" + env.name + " server] can't connect.")
        return False
    return True


# Script starts
parser = argparse.ArgumentParser(description="Dokkan WT fetch module")
parser.add_argument("-a", "--account", type=str, required=True, help="Dokkan account that will use for fetches")
parser.add_argument("-d", "--delay", type=int, default=15, help="Delay between fetches (recommended 5-7)")
parser.add_argument("-e", "--edition", type=int, default=58, help="WT edition")
parser.add_argument("-f", "--fetch", type=int, default=1000, help="Amount of players per fetch (minimum 100)")
parser.add_argument("-p", "--path", type=str, default="fetches", help="Path to the fetches")
args = parser.parse_args()

ACCOUNT = args.account
FETCH_SZ = args.fetch
DELAY = args.delay
WT_EDITION = args.edition
SAVE_PATH = args.path

print("Account selected:", ACCOUNT)
print("Fetch size:", FETCH_SZ)
print("Delay:", DELAY)
print("WT Edition:", WT_EDITION)
print("Path:", SAVE_PATH)

if check_servers(config.game_env):
    # Creates directory if not exists
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    while True:
        # Login account (light version)
        load_fetch.run(ACCOUNT)

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
        else:
            fetch = wt.run(FETCH_SZ, WT_EDITION)
            with open(os.path.join(SAVE_PATH, f"{LATEST_FETCH}.json"), "w") as e:
                json.dump(fetch, e, indent=3)
            LATEST_FETCH += 1

        time.sleep(60 * DELAY)
else:
    print(Fore.RED + "press ENTER to close...")
    input()
    exit()
