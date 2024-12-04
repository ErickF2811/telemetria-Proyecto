import requests
from flask import Flask, render_template, request
import json
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    
    return render_template('index.html')



