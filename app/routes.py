from flask import render_template, request
from app import app
from app import api_requests


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/handle_data", methods=["POST"])
def handle_data():
    username = request.form["username"]
    platform = request.form["platform"]
    player = api_requests.PlayerInfo(username, platform)
    kills = int(player.kills)
    assists = int(player.assists)
    return render_template("home.html", username=username, kills=kills, assists=assists)