#Kyle Liu, Yu Lu, Emily Mai, Jun Jie Li
#whospm

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

@app.route("/chart", methods=['GET', 'POST'])
def homepage():
    flash("Welcome to Organituanas!!")
    return render_template("chart.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
