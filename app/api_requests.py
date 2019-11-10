import requests
import json
import os

HEADERS = {"X-API-Key": os.environ["BUNGIE_API_KEY"]}


class PlayerInfo():
        
    def __init__(self, username, platform):
        self.username = username
        self.platform = platform
        self.membership_id = ""
        self.membership_type = ""
        self.kills = ""
        self.assists = ""
        self.get_player()
        self.get_historical_stats()
        
    def get_manifest(self):
        
        # Get manifest URL
        r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest").json()
        manifest_link = r["Response"]["jsonWorldContentPaths"]["en"]
                  
        # Download the file
        r = requests.get("https://www.bungie.net/" + manifest_link).json()
        with open("man.json", "w") as f:
            json.dump(r, f, indent=2)
            
    def get_player(self):
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/{self.platform}/{self.username}", headers=HEADERS)

        player_json = r.json()
        self.membership_id = player_json["Response"][0]["membershipId"]
        self.membership_type = player_json["Response"][0]["membershipType"]
        
    def get_historical_stats(self):
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/{self.membership_type}/Account/{self.membership_id}/Stats", headers=HEADERS).json()
        
        self.kills = r["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["kills"]["basic"]["value"]
        self.assists = r["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]["assists"]["basic"]["value"]