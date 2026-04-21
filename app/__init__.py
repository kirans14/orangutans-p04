#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

# Imports >>
from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
from db import select_query, insert_query, general_query
from api import get_games_and_playtime
from recommendations import get_recs
import json
from urllib.request import Request, urlopen
import pprint, os
import random
# import fetcher

# Initialize DB >>

# Create instance of Flask app >>
app = Flask(__name__)
app.secret_key = "ABCEDFGHIJKLMNOPQRSTUVWXYZ12345678909876543216767667"

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
        steam_id = request.args["steam_id"].strip()
        games_and_playtime = get_games_and_playtime(steam_id)
        if games_and_playtime == 0:
            print("a")
            return redirect(url_for("steam_id"))
        game_list = ",".join([str(game) for game in games_and_playtime[0]])
        playtimes = ",".join([str(playtime) for playtime in games_and_playtime[1]])
        # print(game_list)
        # print(playtimes)
        if select_query("SELECT * FROM users WHERE steam_id=?", [steam_id]) != []:
            general_query("UPDATE users SET games=?, playtimes=? WHERE steam_id=?", [game_list, playtimes, steam_id])
        else:
            insert_query("users", {"steam_id": steam_id, "games": game_list, "playtimes": playtimes})
        session["id"] = steam_id
    recs = get_recs(steam_id, 10)
    rec_list = [str(select_query("SELECT name FROM games WHERE app_id=?", [rec])[0]["name"]) for rec in recs]
    return render_template("yourtrends.html", rec_list = rec_list)

@app.get("/logout")
def logout_get():
    general_query("DELETE FROM users WHERE steam_id=?", [session["id"]])
    session.pop("id")
    return redirect(url_for("home_get"))

#neccessary api fetches for charts below
@app.route('/api/ranked/<metric>/<int:limit>')
def get_chart_ranked(metric, limit):
    allowed = {
        'total_positive': 'r.total_positive',
        'total_negative': 'r.total_negative',
        'total_reviews':  'r.total_reviews',
        'price':          'g.price / 100.0' # btw why tf is prioce not in the rviews table
    }
    # parameter checkers
    if metric not in allowed:
        print(f"get_chart_ranked: Hi. '{metric}' is not supported yet! Using 'total_positive' instead")
        metric = 'total_positive'
        
    if not isinstance(limit, int) or limit <= 0:
        print(f"get_chart_ranked: Hi. {limit} is not a positive integer!")
        return jsonify({'error': 'Limit must be a positive integer'}), 400
    db_column = allowed[metric]
    query = f"""
        SELECT g.name, {db_column} AS data, g.app_id 
        FROM Games g
        LEFT JOIN Reviews r ON g.app_id = r.app_id
        ORDER BY {db_column} DESC
        LIMIT {limit};
    """
    results = select_query(query)
    return jsonify({
        'labels': [row['name'] for row in results],
        'data': [row['data'] for row in results],
        'gameids': [row['app_id'] for row in results]
    })

@app.route('/api/counts/<attribute>/<int:limit>')
def get_chart_counts(attribute, limit):
    allowed = {'genre_list', 'tag_list', 'developer', 'publisher'}
    #parameter checkers
    if attribute not in allowed:
        print(f"get_chart_counts: Hi. {attribute} is not on the list of allowed attributes!")
        return jsonify({'error': f'get_chart_counts: Invalid attribute'}), 400
    if not isinstance(limit, int) or limit <= 0:
        print(f"get_chart_ranked: Hi. {limit} is not fa positive integer!")
        return jsonify({'error': f'get_chart_counts: Limit must be a positive integer'}), 400
    
    query = f"SELECT app_id, {attribute} FROM Games WHERE {attribute} IS NOT NULL AND {attribute} != ''"
    results = select_query(query)
    counts = {}
    for row in results:
        val = row[attribute]
        app_id = row['app_id']
        if not val: continue
        # dictionary
        if attribute == 'tag_list':
            try:
                tags_dict = json.loads(val)
                for tag in tags_dict.keys():
                    if tag not in counts:
                        counts[tag] = []
                    counts[tag].append(app_id)
            except Exception:
                continue
        # comma seprated lists (genres, developers, publishers)
        else:
            items = [item.strip() for item in str(val).split(',') if item.strip()]
            for item in items:
                if item not in counts:
                    counts[item] = []
                counts[item].append(app_id)
    
    # sort the dictionary items by the length of their app_id lists (descending order)
    sorted_items = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)[:limit]
    
    return jsonify({
        'labels': [item[0] for item in sorted_items],
        'data': [len(item[1]) for item in sorted_items], # The count is the length of the list
        'gameids': [item[1] for item in sorted_items] # Returning the list of gameids 
    })
@app.route('/api/homepage_recommendation')
def get_homepage_recommendation():
    query = """
        SELECT g.app_id, g.name, g.publisher, g.tag_list, g.genre_list, r.total_positive, r.total_negative
        FROM Games g
        JOIN Reviews r ON g.app_id = r.app_id
        ORDER BY r.total_positive DESC
        LIMIT 500;
    """
    results = select_query(query)
    return jsonify(random.choice(results) if results else {})

@app.route('/api/user_data')
def get_user_data():
    if "id" not in session:
        return jsonify({"error": "User not logged in"}), 401
    steam_id = session["id"]

    #user's raw list of games and playtimes
    user_info = select_query("SELECT games, playtimes FROM users WHERE steam_id=?", [steam_id])
    if not user_info:
        return jsonify({"error": "No user data found"}), 404
    # print(user_info)
    user_games = user_info[0]["games"].split(",")
    user_playtimes = [round(int(p) / 60.0, 2) for p in user_info[0]["playtimes"].split(",")]
    # print(user_games)
    # print(user_playtimes)

    # Create a quick lookup dictionary mapping app_id (as string) to its playtime
    playtime_dict = dict(zip(user_games, user_playtimes))
    placeholders = ",".join(["?"] * len(user_games))
    
    query = f"""
        SELECT g.app_id, g.name, g.genre_list, r.total_positive, r.total_negative 
        FROM games g
        LEFT JOIN reviews r ON g.app_id = r.app_id
        WHERE g.app_id IN ({placeholders})
    """

    game_details = select_query(query, user_games)
    most_played = []
    genre_playtime = {}
    total_pos = 0
    total_neg = 0

    for row in game_details:
        app_id_str = str(row["app_id"])
        if app_id_str not in playtime_dict:
            continue
            
        pt = playtime_dict[app_id_str]

        # most played
        most_played.append({"name": row["name"], "playtime": pt, "app_id": row["app_id"]})

        # playtime by gewnre
        if row["genre_list"]:
            genres = [g.strip() for g in row["genre_list"].split(',') if g.strip()]
            for genre in genres:
                if genre not in genre_playtime:
                    genre_playtime[genre] = 0
                genre_playtime[genre] += pt

        # reviews
        if row["total_positive"]: total_pos += row["total_positive"]
        if row["total_negative"]: total_neg += row["total_negative"]

    # sort most played and genres to get the top 10
    most_played.sort(key=lambda x: x["playtime"], reverse=True)
    top_10_games = most_played[:10]
    
    top_genres = sorted(genre_playtime.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        "most_played": {
            "labels": [g["name"] for g in top_10_games],
            "data": [g["playtime"] for g in top_10_games],
            "app_ids": [g["app_id"] for g in top_10_games]
        },
        "genre_playtime": {
            "labels": [g[0] for g in top_genres],
            "data": [g[1] for g in top_genres]
        },
        "reviews": {
            "labels": ["Positive Reviews", "Negative Reviews"],
            "data": [total_pos, total_neg]
        }
    })
    
if __name__ == "__main__":
    app.run(debug=True)
