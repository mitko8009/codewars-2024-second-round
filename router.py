from flask import Flask, redirect, request
import os
import signal

import database
import utils

app = Flask(__name__)

def run_server() -> None:
    app.run(port=utils.getFromConfig("flask_port"), use_reloader=False, debug=utils.getFromConfig("flask_debug"))

# Redirect to URL from shortcode
@app.route('/<shortcode>', methods=['GET', 'POST'])
def redirect_url(shortcode: str) -> str:
    try:
        url = database.get_url(shortcode)
        metadata = database.getMetadata(shortcode)
    except:
        return "URL not found", 404
    
    if "expires" in metadata.keys() and metadata['expires'] is not None:
        if metadata['expires'] < utils.getTimestamp():
            database.delete_url(shortcode)
            return "URL not found", 404
    
    # If password is set, prompt for password
    if metadata['password'] is not None:
        if request.method == 'POST':
            password = request.form.get('password')
            if password == metadata['password']:
                return redirectUrl(url)
            else:
                return "Incorrect password", 403
        return utils.getFileContents(utils.resource_path("./static/password.html")).format(
            shortcode=shortcode,
            app_title=utils.getFromConfig("title"),
            css=utils.getFileContents(utils.resource_path("./static/style.css")),
            js=utils.getFileContents(utils.resource_path("./static/script.js")),
        )
        
    redirectUrl(url)
    

def redirectUrl(url: str) -> str:
    if url is None:
        return "URL not found", 404
    
    if not url.startswith("http"):
        url = "http://" + url
            
    try:
        return redirect(url)
    except:
        return "URL not found", 404

    
    
def shutdown_server() -> None:
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    from main import main
    main()