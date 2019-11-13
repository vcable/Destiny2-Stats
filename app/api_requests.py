import requests
import json
import os

HEADERS = {"X-API-Key": os.environ["BUNGIE_API_KEY"]}


class PlayerInfo():
        
    def __init__(self, username, platform):
        self.username = username
        self.platform = platform
        self.character_id_list = []
        self.error = ""
            
    def get_player(self):
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/SearchDestinyPlayer/{self.platform}/{self.username}", headers=HEADERS).json()
        
        if len(r["Response"]) == 0:
            self.error = "Player not found."
        else:
            self.error = ""
            self.membership_id = r["Response"][0]["membershipId"]
            self.membership_type = r["Response"][0]["membershipType"]
            
    def get_character(self):
        # Gets profile
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/{self.membership_type}/Profile/{self.membership_id}?components=100", headers=HEADERS).json()
        # Gets all character IDs
        self.character_id_list.append(r["Response"]["profile"]["data"]["characterIds"])
        
        r = requests.get(f"https://www.bungie.net/platform/Destiny2/{self.membership_type}/Profile/{self.membership_id}/Character/{self.character_id_list[0][0]}?components=205", headers=HEADERS).json()
        self.equipped_item_hashes = []
        
        for item in r["Response"]["equipment"]["data"]["items"]:
            self.equipped_item_hashes.append(item["itemHash"])
        
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
            self.light_level = query_base["highestLightLevel"]["basic"]["displayValue"]
        
        
class QueryManifest():
    
    def __init__(self, hash_list):
        self.hash_list = hash_list
        self.equipped_items = {}
        self.display_items = {}
        self.item_query()
        
    def get_manifest(self):
        
        # Get manifest URL
        r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest").json()
        manifest_link = r["Response"]["jsonWorldContentPaths"]["en"]
                  
        # Download the file
        r = requests.get("https://www.bungie.net/" + manifest_link).json()
        with open("man.json", "w") as man:
            json.dump(r, man, indent=2)
            
    def item_query(self):
        for item_hash in self.hash_list:
            r = requests.get(f"https://www.bungie.net/platform/Destiny2/Manifest/DestinyInventoryItemDefinition/{str(item_hash)}", headers=HEADERS).json()
            
            # Adds key/value pair to item_list where key is item name and value is item icon
            self.equipped_items[r["Response"]["displayProperties"]["name"]] = "https://bungie.net" +r["Response"]["displayProperties"]["icon"]

        # Remove last 6 items since they are not weapons/armor
        i = 0
        for key, value in self.equipped_items.items():
            i += 1
            if i <= 11:
                self.display_items[key] = value
            else: 
                break            
            
            