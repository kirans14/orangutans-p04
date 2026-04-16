#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

from db import *

def get_recs(steam_id, number):
    games = select_query("SELECT games FROM players WHERE steam_id=?", [steam_id]).split(",")
    playtimes = select_query("SELECT playtimes FROM players WHERE steam_id=?", [steam_id]).split(",")
    for i in range(games):
        pass 
    # weight e/ tag by cumulative playtime of games in user's library with the tag
    # take the most heavily weighted tags and go down store list, from most to least positively reviewed
    # pick games with most similar tags, assuming they arent already owned:
    #     prioritize filling all n rec "slots" first and swap games out when encountering one that matches better
    #     once sufficiently close to tags or reaching end of store list, return games
    # potentially look at player's recently played games? --> weight more heavily
    rec = 0
    return rec