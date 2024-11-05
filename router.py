from flask import Flask, redirect
import threading
import requests
import sys
import os
import signal

from init import *
import database

app = Flask(__name__)

def run_server():
    app.run(port=5000, use_reloader=False)


@app.route('/<shortcode>')
def redirect_url(shortcode):
    url = database.get_url(shortcode)
    if url is None:
        return "URL not found", 404
    
    if not url.startswith("http"):
        url = "http://" + url
            
    try:
        return redirect(url)
    except:
        return "URL not found"
    
    
def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    from main import window
    window()