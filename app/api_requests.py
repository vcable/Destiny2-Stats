import requests
import json
import os

HEADERS = {"X-API-Key": os.environ["BUNGIE_API_KEY"]}


class PlayerInfo():
        
    def __init__(self, username, platform):
        self.username = username
        self.platform = platform
        self.error = ""
            
    def get_player(self):
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/{self.platform}/{self.username}", headers=HEADERS).json()
        
        if len(r["Response"]) == 0:
            self.error = "Player not found."
        else:
            self.error = ""
            self.membership_id = r["Response"][0]["membershipId"]
            self.membership_type = r["Response"][0]["membershipType"]
            
        
    def get_stats(self):
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/{self.membership_type}/Account/{self.membership_id}/Stats", headers=HEADERS).json()
        
        if not r["Response"]["mergedAllCharacters"]["results"]["allPvP"]:
            self.error = "Player has no PvP stats"
        else:
            self.error = ""
            query_base = r["Response"]["mergedAllCharacters"]["results"]["allPvP"]["allTime"]
            self.kills = query_base["kills"]["basic"]["displayValue"]
            self.assists = query_base["assists"]["basic"]["displayValue"]
            self.total_matches = query_base["activitiesEntered"]["basic"]["displayValue"]
            self.wins = query_base["activitiesWon"]["basic"]["displayValue"]
            self.time_played = query_base["secondsPlayed"]["basic"]["displayValue"]
        
        
        
        
        
        
def get_manifest():
        
        # Get manifest URL
        r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest").json()
        manifest_link = r["Response"]["jsonWorldContentPaths"]["en"]
                  
        # Download the file
        r = requests.get("https://www.bungie.net/" + manifest_link).json()
        with open("man.json", "w") as f:
            json.dump(r, f, indent=2)