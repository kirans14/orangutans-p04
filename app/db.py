# Orangutans
# Kiran Soemardjo, Eviss Wu, Mustafa Abdullah, Yu Lu
# SoftDev

import sqlite3
import json
from datetime import datetime
import os
from urllib.request import Request, urlopen
import pprint
import re

DB_FILE="./data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)

#returns as list of dicts, where each item in the list is one row's entry, and each dict entry contains the selected data as the value for the column name as the key
def select_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    out_array = []
    column_names = c.description
    for row in c.fetchall():
        item_dict = dict()
        for col in range(len(row)):
             item_dict.update({column_names[col][0]: row[col]})
        out_array.append(item_dict)
    c.close()
    db.commit()
    return out_array

def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)}) RETURNING *;", tuple(data.values()))
    row = c.fetchall()
    output = dict()
    for col in range(len(row[0])):
        output.update({c.description[col][0]: row[0][col]})
    c.close()
    db.commit()
    return output

def general_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    c.close()
    db.commit()
    
def get_steam_description(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    req = urllib.request.Request(url, headers={"User Agent": "Mozilla/5.0"})
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
            tag_list     TEXT
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
            games          TEXT ,
            playtime       DOUBLE
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

    for app_id, g in data.items():

        price = g.get("price", 0)

        genre_list = g.get('genre', '')

        tags = g.get('tags', {})

        sorted_items = sorted(tags.keys(), key=lambda x: x[1], reverse=True)

        keys_items = []

        for key, value in sorted_items:
            keys_items.append(key)
        
        tag_list = keys_items

        insert_query("Games", {
            "app_id":      str(app_id),
            "name":        g.get("name", ""),
            "release_date": None,            
            "developer":   g.get("developer", ""),
            "publisher":   g.get("publisher", ""),
            "is_free":     None,
            "price":       price,
            "description": None,           
            "genre_list":  genre_list,
            "tag_list":    None,
        })
    
    return tag_list
    

create_tables()
# pprint.pprint(populate_db("./static/detaileddata.json"))


