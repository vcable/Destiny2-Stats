from flask import Flask
from app import api_requests
import os

IMAGES = os.path.join("static", "img")

app = Flask(__name__)
app.config["IMAGES"] = IMAGES

from app import routes