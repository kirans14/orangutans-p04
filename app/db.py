# Orangutans
# Kiran Soemardjo, Eviss Wu, Mustafa Abdullah, Yu Lu
# SoftDev

import sqlite3
import json
from datetime import datetime
import os

DB_FILE="data.db"

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

def create_tables():
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
            installed_games INTEGER DEFAULT 0,
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

        sorted_items = sorted(tags.items(), key=lambda x: x[1], reverse=True)

        keys_items = []

        for key, value in sorted_items:
            keys_items.append(key)

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


