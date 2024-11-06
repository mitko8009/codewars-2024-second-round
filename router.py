from flask import Flask, redirect
import os
import signal

import database
import utils

app = Flask(__name__)

def run_server() -> None:
    app.run(port=utils.getFromConfig("flask_port"), use_reloader=False, debug=utils.getFromConfig("flask_debug"))


@app.route('/<shortcode>')
def redirect_url(shortcode: str) -> str:
    url = database.get_url(shortcode)
    if url is None:
        return "URL not found", 404
    
    if not url.startswith("http"):
        url = "http://" + url
            
    try:
        return redirect(url)
    except:
        return "URL not found"
    
    
def shutdown_server() -> None:
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == '__main__':
    from main import window
    window()