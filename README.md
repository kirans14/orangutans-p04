# orangutans-p04

## Roster:
**Kiran Soemardjo** -  Project Manager <br>
Flask functionality, Filtering, sorting, and recommendations<br>
<br>
**Mustafa Abdullah** -  Database manager<br>
builds and maintains Sqlite database + integration with middleware<br>
<br>
**Yu Lu** -  Middleware <br>
Flask functionality, Visualize data with chart.js<br>
<br>
**Eviss Wu** - Front-end <br>
Frontend visuals with Bootstrap, Jinja in HTML templates, and page routing<br>
<br>

## Description:
We plan to pull data from the Steam API, and use the data to visualize trends in the games that are popular at the moment. The data will also be filterable/sortable by rating, player count, genre, tag, etc. Additionally, the user will be able to enter their Steam ID, and get recommendations based on the games in their library, as well as an analysis of personal trends (through the Steam API using the user’s ID).

#### Visit our live site at [http://192.81.214.53:1000/](http://192.81.214.53:1000/)

## Install Guide:
>1) Git clone this repo through ssh (`git@github.com:kirans14/orangutans-p04.git`) onto local computer in an accessible location
>2) Navigate into cloned Repo [`cd orangutans-p04/`]. Then navigate into `app` directory [`cd app`]

>3) Create a python virtual enviornment using: [`python3 -m venv venv`].
>Activate virtual enviornment using: [`cd venv`] Then `. bin/activate`

>4) Navigate to root of repo `orangutans-p04/` via: [`cd ..`] (2x) to prepare for installation of dependencies
>5) Install required dependencies using command: [`pip install -r requirements.txt`] then navigate into `app` via [`cd app`] to prepare to launch


# Launch Codes:
- Run command: [`python3 __init__.py`] or [`python __init__.py`]
> Ensure current terminal PATH is correctly routed to `orangutans-p04/app` if not, route to `app` using command: [`cd (Directory you installed our repo into)/orangutans-p04/app`]
