#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

import json
import requests
import re
import urllib

def get_api_key():
    api_key = ""
    try:
        with open("keys/api_key.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError as e:
        print("API key not valid")
    return api_key
 
# returns list containing two lists: one for user's games, and one for playtimes
def get_games_and_playtime(steam_id: str) -> list:
    try:
        response = requests.get(
            "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
            params={
                "key": get_api_key(),
                "steamid": steam_id,
                "include_appinfo": 1,
                "include_played_free_games": 1,
                "format": "json",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json().get("response", {})
        games = data.get("games")
        if not games:
            return None
        return [[g["appid"] for g in games], [g["playtime_forever"] for g in games]]
    except Exception:
        return None

# def get_game_playtime(steam_id, app_id):
#     params = {
#         "key": get_api_key(),
#         "steamid": steam_id,
#         "include_appinfo": 1,
#         "include_played_free_games": 1,
#         "format": "json"
#     }
#     games = requests.get(
#         "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
#         params=params
#     ).json().get("response", {}).get("games", [])

#     for game in games:
#         if game["appid"] == app_id:
#             print(game.get("playtime_forever",0))
#             return game.get("playtime_forever", 0)
#     return 0

# def get_game_playtime(steam_id, app_id):
#     response = requests.get(
#         "https://api.steampowered.com/IPlayerService/GetSingleGamePlaytime/v1/",
#         params={
#             "key": get_api_key(),
#             "steamid": steam_id,
#             "appid": app_id
#         }
#     )
#     response.raise_for_status()
#     playtime = response.json()[]

def get_steam_tags() -> list[str] | None:
    response = requests.get(
        "https://api.steampowered.com/IStoreService/GetTagList/v1/",
        params={"key": get_api_key(), "language": "english"}
    )
    #rate limited
    if response.status_code == 429:
        return None
    data = response.json()["response"]["tags"]
    tag_list = [tag["name"].replace("-", " ") for tag in data]
    tag_list.sort()
    # if not data.get("success"):
    #     return None
    # categories = [c["description"] for c in data["data"].get("categories", [])]
    # genres = [g["description"] for g in data["data"].get("genres", [])]
    return tag_list

def parse_owners(str):
    lower = str.split("..")[0].strip()

    return int(lower.replace(",", ""))

def get_steam_description(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read().decode())
    app = data.get(str(app_id), {})
    if not app.get("success"):
        return f"No game found for App ID {app_id}."
    info = app["data"]
    name = info.get("name", "Unknown")
    raw = info.get("detailed_description") or info.get("short_description", "")
    desc = re.sub(r"<br\s/?>", "\n", raw, flags=re.IGNORECASE)
    desc = re.sub(r"</?(p|li|ul|ol|h[1-6]|div)[^>]>", "\n", desc, flags=re.IGNORECASE)
    desc = re.sub(r"<[^>]+>", "", desc)
    desc = re.sub(r"\n{3,}", "\n\n", desc).strip()
    return f"{name}\n\n{desc}"    

# with open("./static/detaileddata.json") as f:
#     data = json.load(f)

# games = list(data.values())

# sorted_games = sorted(games,key=lambda g: parse_owners(g["owners"]),reverse=True)

# for rank, game in enumerate(sorted_games, start=1):
#     print(f"{rank}. {game['name']} {game['owners']}")
