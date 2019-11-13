from flask import render_template, request
from app import app
from app import api_requests
import os

logo = os.path.join(app.config["IMAGES"], 'logo.png')

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", logo=logo)


@app.route("/show_stats", methods=["POST"])
def get_stats():
    username = request.form["username"]
    platform = request.form["platform"]
    player = api_requests.PlayerInfo(username, platform)
    player.get_player()
    if player.error == "Player not found.":
        error = player.error
        return render_template("error.html", error=error)
    else:
        player.get_stats()
        if player.error == "Player has no PvP stats":
            error = player.error
            return render_template("error.html", error=error)
        else:
            player.get_character()
            kills = player.kills
            assists = player.assists
            time_played = player.time_played
            total_matches = player.total_matches
            wins = player.wins
            light_level = player.light_level
            error = player.error
            item_hashes = player.equipped_item_hashes
            items = api_requests.QueryManifest(item_hashes)
            equipped_items = items.display_items
            
            return render_template("show_stats.html", username=username, kills=kills, assists=assists, error=error,
                                    wins=wins, time_played=time_played, total_matches=total_matches, light_level=light_level,
                                    equipped_items=equipped_items, logo=logo)
        

    
  
    