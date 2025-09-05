
# GUI de control y monitoreo para robot de desinfección con luz UVC

from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__)

@app.route('/')

def index():
    return render_template()
