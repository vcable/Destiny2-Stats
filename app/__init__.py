from flask import Flask
from app import api_requests

app = Flask(__name__)

from app import routes