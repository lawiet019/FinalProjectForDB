from flask import Flask
#init an app
app = Flask(__name__)

from app import routes
