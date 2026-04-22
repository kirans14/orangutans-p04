#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

from db import select_query, insert_query, general_query
from api import get_steam_tags
import json
import math

def get_recs(steam_id, number):
    games = select_query("SELECT games FROM users WHERE steam_id=?", [steam_id])[0]["games"].split(",")
    playtimes = select_query("SELECT playtimes FROM users WHERE steam_id=?", [steam_id])[0]["playtimes"].split(",")
    tag_list = get_steam_tags()
    # print(tag_list)
    user_vector = [0.0] * len(tag_list)
    game_ids = [game["app_id"] for game in select_query("SELECT app_id FROM games")]
    for i in range(len(games)):
        if games[i] not in game_ids:
            continue
        # print(select_query("SELECT tag_list FROM games WHERE app_id=?", [games[i]]))
        # print(games[i])
        # print(json.loads(select_query("SELECT tag_list FROM games WHERE app_id=?", [games[i]])[0]["tag_list"]).keys())
        game_tags = json.loads(select_query("SELECT tag_list FROM games WHERE app_id=?", [games[i]])[0]["tag_list"]).keys()
        for tag in game_tags:
        #     if tag == "Rogue-like":
        #         tag = "Roguelike"
        #     if tag == "Rogue-lite":
        #         tag = "Roguelite"
            user_vector[tag_list.index(tag)] += int(playtimes[i])
    # case for when norm is zero
    user_norm = math.sqrt(sum(value * value for value in user_vector))
    if user_norm != 0:
        user_vector = [value / user_norm for value in user_vector]
    # print(tag_list)
    print(user_vector)

    recs = {}
    for game in game_ids:
        if game in games:
            continue
        game_vector = [float(i) for i in select_query("SELECT tag_vector FROM games WHERE app_id=?", [game])[0]["tag_vector"].split(",")]
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(user_vector, game_vector)))
        if len(recs) < number:
            recs[game] = distance
            continue
        farthest = max(recs.keys(), key=recs.get) #returns key corresponding to max distance
        if distance < recs[farthest]:
            recs.pop(farthest)
            recs[game] = distance
    print(recs.keys())
    for rec in recs:
        print(select_query("SELECT name FROM games WHERE app_id=?", [rec])[0]["name"])
    
    out={}
    for rec in recs:
        tag_list = list(json.loads(select_query("SELECT tag_list FROM games WHERE app_id=?", [rec])[0]["tag_list"]).keys())
        common_tags = []
        for i in range(len(tag_list)):
            if user_vector[i] != 0:
                common_tags.append(tag_list[i])
            if len(common_tags) == 3:
                break
        out[rec] = common_tags
    return out

