#Kiran Soemardjo, Mustafa Abdullah, Yu Lu, Eviss Wu
#Orangutans

# Imports >>
from flask import Flask, render_template, request, flash, url_for, redirect, session
import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O
##import db
import json
from urllib.request import Request, urlopen
import pprint
import os
import re
import fetcher

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
    return render_template("home.html")

@app.route("/chart", methods=['GET', 'POST'])
def chart_get():
    with open("static/data/tempdata.json", "r") as f:
        data = json.load(f)
    return render_template("chart.html", data=data)

@app.get("/steam_id")
def id_get():
    return render_template("id.html")

@app.post("/steam_id")
def id_post():
    steam_id = request.args["id"]
    session["id"] = steam_id
    return render_template("id.html", id=steam_id)

if __name__ == "__main__":
    app.run(debug=True)
