#!/usr/bin/env python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)