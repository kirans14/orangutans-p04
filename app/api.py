import json

def parse_owners(str):
    lower = str.split("..")[0].strip()

    return int(lower.replace(",", ""))


with open("./static/detaileddata.json") as f:
    data = json.load(f)

games = list(data.values())

sorted_games = sorted(games,key=lambda g: parse_owners(g["owners"]),reverse=True)

for rank, game in enumerate(sorted_games[:20], start=1):
    print(f"{rank}. {game['name']} {game['owners']}")
