#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

# Imports >>
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
from db import select_query, insert_query, general_query
from api import get_games_and_playtime
from recommendations import get_recs
import json
from urllib.request import Request, urlopen
import pprint, os, re
# import fetcher

# Initialize DB >>

# Create instance of Flask app >>
app = Flask(__name__)
app.secret_key = "ABCEDFGHIJKLMNOPQRSTUVWXYZ1234567890987654321"

@app.context_processor
def user_context(): # persistent info made avalible for all html templates
    return {
    }

#@app.before_request

# ROUTING BEGINS >>

@app.get("/")
def home_get():
    with open("static/detaileddata.json", "r") as f:
        data = json.load(f)
    return render_template("home.html", data=data)

@app.route("/chart", methods=['GET', 'POST'])
def chart_get():
    with open("static/data/tempdata.json", "r") as f:
        data = json.load(f)
    return render_template("chart.html", data=data)

@app.get("/steam_id")
def id_get():
    if "id" not in session:
        return render_template("id.html")
    return redirect(url_for("trends_get"))

# ADD VERIFICATION OF STEAMID
@app.get("/trends")
def trends_get():
    if "id" in session:
        steam_id = session["id"]
    else:
        steam_id = request.args["steam_id"]
        session["id"] = steam_id
        games_and_playtime = get_games_and_playtime(steam_id)
        game_list = ",".join([str(game) for game in games_and_playtime[0]])
        playtimes = ",".join([str(playtime) for playtime in games_and_playtime[1]])
        # print(game_list)
        # print(playtimes)
        if select_query("SELECT * FROM users WHERE steam_id=?", [steam_id]) != []:
            general_query("UPDATE users SET games=?, playtimes=? WHERE steam_id=?", [game_list, playtimes, steam_id])
        else:
            insert_query("users", {"steam_id": steam_id, "games": game_list, "playtimes": playtimes})
    recs = get_recs(steam_id, 10)
    return render_template("trends.html", recs = recs)

# trends_post method for deleting id --> pop from session and redirect to /steam_id

if __name__ == "__main__":
    app.run(debug=True)
