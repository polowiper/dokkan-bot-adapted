from pathlib import Path

import config
from classes.Game import GameAccount
from colorama import Fore, Style
from services.account import AccountService

NAME = "load_fetch"
DESCRIPTION = "Load a save (only fetch data version)"
CONTEXT = [config.GameContext.AUTH]


def run(file_name: str):
    file_path = Path(config.ROOT_DIR, "saves", file_name + ".json")
    if not file_path.exists():
        print(Fore.RED + Style.BRIGHT + "Could not find " + file_name)
        return

    config.game_account = GameAccount.from_file(file_path)
    config.game_account = AccountService.login(config.game_account)
    print(Fore.GREEN + "Welcome back" + Style.RESET_ALL)
    config.game_account.to_file(file_path)
