# Orangutans
# Kiran Soemardjo, Eviss Wu, Mustafa Abdullah, Yu Lu
# SoftDev

from api import get_steam_tags, get_steam_description
from db import general_query, insert_query, select_query
import json
import numpy

def create_tables():
    general_query("DROP TABLE IF EXISTS Games;")
    general_query("DROP TABLE IF EXISTS Player_stats;")
    general_query("DROP TABLE IF EXISTS Users;")
    general_query("DROP TABLE IF EXISTS Reviews;")

    general_query("""
        CREATE TABLE IF NOT EXISTS Games (
            app_id       TEXT PRIMARY KEY,
            name         TEXT,
            release_date TEXT,
            developer    TEXT,
            publisher    TEXT,
            is_free      BOOLEAN,
            price        DOUBLE,
            description  TEXT,
            genre_list   TEXT,
            tag_list     TEXT,
            tag_vector   TEXT
        );
    """)

    general_query("""
        CREATE TABLE IF NOT EXISTS Player_stats (
            app_id             INTEGER,
            current_players    INTEGER,
            peak_players_today INTEGER,
            time_fetched       TEXT,
            FOREIGN KEY (app_id) REFERENCES Games(app_id)
        );
    """)

    general_query("""
        CREATE TABLE IF NOT EXISTS Users (
            steam_id       TEXT PRIMARY KEY,
            api_key        TEXT,
            games          TEXT,
            playtimes      TEXT
        );
    """)

    general_query("""
        CREATE TABLE IF NOT EXISTS Reviews (
            app_id           INTEGER,
            review_score     INTEGER,
            review_score_desc TEXT,
            total_positive   INTEGER,
            total_negative   INTEGER,
            total_reviews    INTEGER,
            FOREIGN KEY (app_id) REFERENCES Games(app_id)
        );
    """)

def populate_db(path):

    with open(path) as f:
        data = json.load(f)
    tag_list = get_steam_tags()
    for app_id, g in data.items():

        price = g.get("price", '')
        price_dollars = int(price) / 100.0 if str(price).isdigit() else 0
        is_free = price_dollars == 0

        genre_list = g.get('genre', '')

        tags = g.get('tags', {})
        # if tags:

        #     sorted_items = sorted(tags.items(), key=lambda x: x[1], reverse=True)

        #     keys_items = []
        #     values_items = []

        #     for key, value in sorted_items:
        #         keys_items.append(key)
        #         values_items.append(value)
            
        #     tag_list = ", ".join(keys_items)
        # else:
        #     tag_list = ''
        print(tags)
        new = []
        for tag in tags:
            if tag == "Rogue-like":
                new.append("Roguelike")
            elif tag == "Rogue-lite":
                new.append("Roguelite")
            elif tag == "e-sports":
                new.append("eSports")
            else: 
                new.append(tag.replace("-", " "))
        if tags != []:
            tags = dict(zip(new, tags.values()))
            if "Masterpiece" in tags.keys():
                tags.pop("Masterpiece")

        tags_string = json.dumps(tags)
        tag_vector = numpy.array([0.0] * len(tag_list))
        for tag in tags:
            tag_vector[tag_list.index(tag)] += int(tags[tag])
        if numpy.linalg.norm(tag_vector) != 0:
            tag_vector /= numpy.linalg.norm(tag_vector)
        print(app_id) 

        insert_query("Games", {
            "app_id":      str(app_id),
            "name":        g.get("name", ""),
            "release_date": None,            
            "developer":   g.get("developer", ""),
            "publisher":   g.get("publisher", ""),
            "is_free":     is_free,
            "price":       price,
            "description": get_steam_description(app_id),           
            "genre_list":  genre_list,
            "tag_list":    tags_string,
            "tag_vector":  ",".join(str(value) for value in tag_vector)
        })
    
        
#         insert_query("Players", {
#             "app_id":      str(app_id),
#             "name":        g.get("name", ""),
#             "release_date": None,            
#             "developer":   g.get("developer", ""),
#             "publisher":   g.get("publisher", ""),
#             "is_free":     None,
#             "price":       price_dollars,
#             "description": None,           
#             "genre_list":  genre_list,
#             "tag_list":    tags_string,
#             "tag_vector":  ",".join(str(value) for value in tag_vector)
#         })
        
        positive = g.get('positive', 0)
        negative = g.get('negative', 0)
        total = positive + negative
        insert_query("Reviews", {
            "app_id":      str(app_id),
            "review_score":        g.get("name", ""),
            "total_positive":    positive,            
            "total_negative":   negative,
            "total_review":   total,
            "current_players":    g.get('ccu', 0)
        })
    
    return tags
    

create_tables()
print(populate_db("./static/detaileddata.json"))