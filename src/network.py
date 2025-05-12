import json
import urllib.parse
from typing import Any, Optional

import requests
from colorama import Fore
from requests import Response

import config
import crypto
from classes.Game import GamePlatform


def __generate_headers(
    method: str,
    endpoint: str,
    platform: GamePlatform = config.game_platform,
    client_version: str = config.game_env.version_code,
    language: str = "en",
    asset_version: str = "////",
    database_version: str = "////",
) -> "dict[str: any]":
    return {
        "User-Agent": platform.user_agent,
        "Accept": "*/*",
        "Authorization": crypto.mac(method, endpoint),
        "Content-type": "application/json",
        "X-Platform": platform.name,
        "X-AssetVersion": asset_version,
        "X-DatabaseVersion": database_version,
        "X-ClientVersion": client_version,
        "X-Language": language,
    }


def __purge_none(data: Optional[dict] = None) -> Optional[dict]:
    if data is None:
        return data
    _copy = data.copy()

    for key in data:
        if type(data[key]) is dict:
            _copy[key] = __purge_none(_copy[key])
        if _copy[key] is None:
            _copy.pop(key)

    return _copy if len(_copy) > 0 else None


def __print_response(res: Response):
    status_color = Fore.RED
    if 100 <= res.status_code <= 199:
        status_color = Fore.BLUE
    elif 200 <= res.status_code <= 299:
        status_color = Fore.GREEN
    elif 300 <= res.status_code <= 399:
        status_color = Fore.YELLOW
    show_content = False
    status_code = "[" + status_color + str(res.status_code) + Fore.RESET + "]"
    url = Fore.GREEN + res.url + Fore.RESET

    print(status_code + " " + res.request.method + " " + url)
    if show_content:
        print(res.text)


def __get(endpoint: str, params: Optional[Any] = None):
    params = __purge_none(params)
    if params is not None:
        endpoint = endpoint + "?" + urllib.parse.urlencode(params)

    url = config.game_env.url + endpoint
    headers = __generate_headers("GET", endpoint)
    res = requests.get(url, headers=headers)
    __print_response(res)
    return res.json() if res.status_code != 204 else None


def __put(endpoint: str, data: Optional[dict[str, Any]] = None):
    headers = __generate_headers("PUT", endpoint)
    url = config.game_env.url + endpoint
    data = __purge_none(data)
    res = requests.put(
        url, headers=headers, data=json.dumps(data) if data is not None else None
    )
    __print_response(res)
    return res.json() if res.status_code != 204 else None


def __post(endpoint: str, data: Optional[dict[str, Any]] = None):
    headers = __generate_headers("POST", endpoint)
    url = config.game_env.url + endpoint
    data = __purge_none(data)
    res = requests.post(
        url, headers=headers, data=json.dumps(data) if data is not None else None
    )
    __print_response(res)
    return res.json() if res.status_code != 204 else None


def get_user():
    return __get("/user")


def get_client_assets_database():
    return __get("/client_assets/database")


def get_gifts():
    return __get("/gifts")


def get_missions():
    return __get("/missions")


def get_budokai_rankings(budokai_id: int, per_page: int = 100, page: int = 1):
    return __get(
        f"/budokais/{budokai_id}/rankings", params={"per": per_page, "page": page}
    )


def get_resources_home(
    apologies: bool = False,
    banners: bool = False,
    bonus_schedules: bool = False,
    budokai: bool = False,
    dragonball_sets: bool = False,
    gifts: bool = False,
    login_bonuses: bool = False,
    missions: bool = False,
    random_login_bonuses: bool = False,
    rmbattles: bool = False,
    user_subscription: bool = False,
    comeback_campaigns: bool = False,
):
    return __get(
        "/resources/home",
        {
            "apologies": str(apologies).lower(),
            "banners": str(banners).lower(),
            "bonus_schedules": str(bonus_schedules).lower(),
            "budokai": str(budokai).lower(),
            "dragonball_sets": str(dragonball_sets).lower(),
            "gifts": str(gifts).lower(),
            "login_bonuses": str(login_bonuses).lower(),
            "missions": str(missions).lower(),
            "random_login_bonuses": str(random_login_bonuses).lower(),
            "rmbattles": str(rmbattles).lower(),
            "user_subscription": str(user_subscription).lower(),
            "comeback_campaigns": str(comeback_campaigns).lower(),
        },
    )


def get_resources_login(
    act_items: bool = False,
    announcements: bool = False,
    awakening_items: bool = False,
    budokai: bool = False,
    card_sticker_items: bool = False,
    card_tags: bool = False,
    cards: bool = False,
    chain_battles: bool = False,
    comeback_campaigns: bool = False,
    cooperation_campaigns: bool = False,
    dragonball_sets: bool = False,
    equipment_skill_items: bool = False,
    eventkagi_items: bool = False,
    friendships: bool = False,
    gashas: bool = False,
    gifts: bool = False,
    joint_campaigns: bool = False,
    login_bonuses: bool = False,
    login_movies: bool = False,
    login_popups: bool = False,
    missions: bool = False,
    potential_items: bool = False,
    rmbattles: bool = False,
    sd_battle: bool = False,
    sd_characters: bool = False,
    sd_packs: bool = False,
    secret_treasure_boxes: bool = False,
    shops_treasure_items: bool = False,
    sns_campaign: bool = False,
    support_films: bool = False,
    support_items: bool = False,
    support_leaders: bool = False,
    support_memories: bool = False,
    teams: bool = False,
    training_fields: bool = False,
    training_items: bool = False,
    treasure_items: bool = False,
    user_areas: bool = False,
    user_card_updated_at: bool = False,
    user_subscription: bool = False,
    wallpaper_items: bool = False,
    special_items: bool = False,
):
    return __get(
        "/resources/login",
        {
            "potential_items": str(potential_items).lower(),
            "training_items": str(training_items).lower(),
            "support_items": str(support_items).lower(),
            "treasure_items": str(treasure_items).lower(),
            "special_items": str(special_items).lower(),
            "sd/battle": str(sd_battle).lower(),
            "sd/characters": str(sd_characters).lower(),
            "sd/packs": str(sd_packs).lower(),
            "shop/treasure/items": str(shops_treasure_items).lower(),
            "user_areas": str(user_areas).lower(),
            "user_card_updated_at": str(user_card_updated_at).lower(),
            "user_subscription": str(user_subscription).lower(),
            "wallpaper_items": str(wallpaper_items).lower(),
            "support_leaders": str(support_leaders).lower(),
            "support_memories": str(support_memories).lower(),
            "teams": str(teams).lower(),
            "training_fields": str(training_fields).lower(),
            "sns_campaign": str(sns_campaign).lower(),
            "support_films": str(support_films).lower(),
            "secret_treasure_boxes": str(secret_treasure_boxes).lower(),
            "rmbattles": str(rmbattles).lower(),
            "act_items": str(act_items).lower(),
            "announcements": str(announcements).lower(),
            "awakening_items": str(awakening_items).lower(),
            "budokai": str(budokai).lower(),
            "card_sticker_items": str(card_sticker_items).lower(),
            "card_tags": str(card_tags).lower(),
            "cards": str(cards).lower(),
            "chain_battles": str(chain_battles).lower(),
            "comeback_campaigns": str(comeback_campaigns).lower(),
            "cooperation_campaigns": str(cooperation_campaigns).lower(),
            "dragonball_sets": str(dragonball_sets).lower(),
            "equipment_skill_items": str(equipment_skill_items).lower(),
            "eventkagi_items": str(eventkagi_items).lower(),
            "friendships": str(friendships).lower(),
            "gashas": str(gashas).lower(),
            "gifts": str(gifts).lower(),
            "joint_campaigns": str(joint_campaigns).lower(),
            "login_bonuses": str(login_bonuses).lower(),
            "login_movies": str(login_movies).lower(),
            "login_popups": str(login_popups).lower(),
            "missions": str(missions).lower(),
        },
    )


def put_user(name: Optional[str] = None, is_ondemand: Optional[bool] = None):
    return __put("/user", {"user": {"name": name, "is_ondemand": is_ondemand}})


def put_tutorial_finish():
    return __put("/tutorial/finish")


def put_tutorial(progress: int):
    return __put("/tutorial", {"progress": progress})


def put_apologies_accept():
    return __put("/apologies/accept")


def post_auth_signup(unique_id: str, captcha_session_key: Optional[str] = None):
    headers = {
        "User-Agent": config.game_platform.user_agent,
        "Accept": "*/*",
        "Content-type": "application/json",
        "X-Platform": config.game_platform.name,
        "X-ClientVersion": config.game_env.version_code,
    }

    data = __purge_none(
        {
            "bundle_id": config.game_env.bundle_id,
            "device_token": "failed" if captcha_session_key is None else None,
            "reason": "NETWORK_ERROR: null" if captcha_session_key is None else None,
            "captcha_session_key": captcha_session_key,
            "user_account": {
                "ad_id": "",
                "unique_id": unique_id,
                "country": config.game_env.country,
                "currency": config.game_env.currency,
                "device": config.game_platform.device_name,
                "device_model": config.game_platform.device_model,
                "os_version": config.game_platform.os_version,
                "platform": config.game_platform.name,
            },
        }
    )

    url = config.game_env.url + "/auth/sign_up"
    res = requests.post(url, headers=headers, data=json.dumps(data))
    __print_response(res)
    return res.json()


def post_auth_signin(
    authorization: str, unique_id: str, captcha_session_key: Optional[str] = None
):
    data = json.dumps(
        __purge_none(
            {
                "bundle_id": config.game_env.bundle_id,
                "device_token": "failed" if captcha_session_key is None else None,
                "reason": (
                    "NETWORK_ERROR: null" if captcha_session_key is None else None
                ),
                "captcha_session_key": captcha_session_key,
                "user_account": {
                    "ad_id": "",
                    "device": config.game_platform.device_name,
                    "device_model": config.game_platform.device_model,
                    "os_version": config.game_platform.os_version,
                    "platform": config.game_platform.name,
                    "unique_id": unique_id,
                },
            }
        )
    )

    headers = __purge_none(
        {
            "User-Agent": config.game_platform.user_agent,
            "Accept": "*/*",
            "Authorization": authorization,
            "Content-type": "application/json",
            "X-ClientVersion": config.game_env.version_code,
            "X-Language": "en",
            "X-UserCountry": config.game_env.country,
            "X-UserCurrency": config.game_env.currency,
            "X-Platform": config.game_platform.name,
        }
    )

    url = config.game_env.url + "/auth/sign_in"
    res = requests.post(url, headers=headers, data=data)
    __print_response(res)
    return res.json()


def post_login_bonuses_accept():
    return __post("/login_bonuses/accept")


def post_gifts_accept(gift_ids: list):
    return __post("/gifts/accept", {"gift_ids": gift_ids})


def post_missions_accept(mission_ids: list):
    return __post("/missions/accept", {"mission_ids": mission_ids})


def post_user_capacity_card():
    return __post("/user/capacity/card")


def post_tutorial_gasha(progress: int):
    return __post("/tutorial/gasha", {"progress": progress})


def post_missions_put_forward():
    return __post("/missions/put_forward")
