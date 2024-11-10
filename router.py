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
def URLRoute(shortcode: str) -> str:
    try:
        url = database.get_url(shortcode)
        metadata = database.getMetadata(shortcode)
    except:
        return "URL not found", 404
    
    # If URL is expired, return error page
    if "expires" in metadata.keys():
        if metadata['expires'] is not None:
            if metadata['expires'] < utils.getTimestamp():
                database.delete_url(shortcode)
                return utils.getFileContents(utils.resource_path("./static/error.html")).format(
                    app_title=utils.getFromConfig("title"),
                    css=utils.getFileContents(utils.resource_path("./static/style.css")),
                    title="Expired URL",
                    content="This URL has expired and is no longer available."
                )

                    
    if metadata['uses'] is not None and metadata['uses'] <= metadata['maxUses']:
        return utils.getFileContents(utils.resource_path("./static/error.html")).format(
            app_title=utils.getFromConfig("title"),
            css=utils.getFileContents(utils.resource_path("./static/style.css")),
            title="Max Uses Reached",
            content="This URL has reached the maximum number of uses."
        ), 403
    
    # If password is set, prompt for password
    if metadata['password'] is not None:
        if request.method == 'POST':
            password = utils.hashPassword(request.form.get('password'))
            if password == metadata['password']:
                return redirect(url)
            else:
                return "Incorrect password", 403
        return utils.getFileContents(utils.resource_path("./static/password.html")).format(
            shortcode=shortcode,
            app_title=utils.getFromConfig("title"),
            css=utils.getFileContents(utils.resource_path("./static/style.css")),
            js=utils.getFileContents(utils.resource_path("./static/script.js")),
        ), 200
        
    
    if metadata['uses'] is not None:
        metadata['uses'] += 1
    
    database.updateMetadata(shortcode, "uses", metadata['uses'])
        
    return redirect(url), 302
    

def redirect(url: str) -> str:
    if url is None:
        return "URL not found", 404
    
    if not url.startswith("http"):
        url = "https://" + url
        
    # return redirect(url)
    try:
        return redirect(url)
    except:
        return "URL not found", 404


def shutdown_server() -> None:
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    from main import main
    main()