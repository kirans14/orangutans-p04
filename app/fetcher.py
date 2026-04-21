import argparse
import time
import json
import requests
import os

def fetch_page(page):
    resp = requests.get(
        "https://steamspy.com/api.php",
        params={"request": "all", "page": page},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def get_top_appids(start):
    end = start + 100
    pages_needed = max(5, (end // 500) + 2)

    games = {}
    for page in range(pages_needed):
        print(f"Fetching page {page}...")
        games.update(fetch_page(page))
        if page < pages_needed - 1:
            print("Waiting 61s for API rate limit...")
            time.sleep(61)

    ranked = sorted(games.values(), key=lambda g: g.get("ccu", 0), reverse=True)
    return [int(g["appid"]) for g in ranked]

def get_details_from_id(json_file, output_file="static/detaileddata.json"):
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            details = json.load(f)
    else:
        details = {}

    with open(json_file, "r") as f:
        appids = json.load(f)
    
    for index, appid in enumerate(appids, start=1):
        if str(appid) in details:
            continue

        try:  
            print(f"[{index}/{len(appids)}] Fetching appid {appid}...")
            resp = requests.get(
                "https://steamspy.com/api.php",
                params={"request": "appdetails", "appid": appid},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            if data and "name" in data:
                details[appid] = data
            
            if index % 100 == 0:
                print(f"Saving progress at {index} fetches...")
                with open(output_file, "w") as f:
                    json.dump(details, f, indent=4)

            time.sleep(1.1)

        except Exception as e:
            print(f"Error at appid {appid}: {e}")
            time.sleep(5)
        
    with open(output_file, "w") as f:
        json.dump(details, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    args = parser.parse_args()
    
    os.makedirs("static", exist_ok=True)
    get_details_from_id("static/data.json", "static/detaileddata.json")