import sqlite3
import os

DB = sqlite3.connect("Data.database.db")
DB_CURSOR = DB.cursor()
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Games(app_id TEXT PRIMARY KEY, name TEST, release_date TEXT, developer TEXT, publisher TEXT, is_free BOOLEAN, price DOUBLE, description TEXT, genre_list TEXT, tag_list TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS player_stats(app_id INTEGER FOREIGN KEY (app_id) REFERENCES GAMES(app_id), current_players INTEGER, peak_players_today INTEGER, time_fetched TEXT);")
DB_CURSOR.execute("CREATE TABLE IF NOT EXISTS Users(steam_id TEXT PRIMARY_KEY, api_key TEXT, installed_games INTEGER, playtime DOUBLE);")

def add_user():
    pass

def get_user():
    pass

def populate_db():
    pass