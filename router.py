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
        return utils.URLNotFoundRoute()
    
    if url is None:
        return utils.URLNotFoundRoute()
    
    if not url.startswith("http"):
        url = "https://" + url
    
    # If URL is expired, return error page
    if "expires" in metadata.keys():
        if metadata['expires'] is not None:
            if metadata['expires'] < utils.getTimestamp():
                database.hideUrl(shortcode)
                return utils.getFileContents(utils.resource_path("./static/error.html")).format(
                    app_title=utils.getFromConfig("title"),
                    css=utils.getFileContents(utils.resource_path("./static/style.css")),
                    title="Expired URL",
                    content="This URL has expired and is no longer available."
                ), 403

    # If max uses is reached, return error page              
    if metadata['maxUses'] is not None and metadata['uses'] >= metadata['maxUses']:
        database.hideUrl(shortcode)
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
                if "uses" in metadata.keys() and metadata['uses'] is not None:
                    metadata['uses'] += 1
                    database.updateMetadata(shortcode, "uses", metadata['uses'])
                
                try:
                    return redirect(url)
                except:
                    return utils.URLNotFoundRoute()
            else:
                return "Incorrect password", 403
        return utils.getFileContents(utils.resource_path("./static/password.html")).format(
            shortcode=shortcode,
            app_title=utils.getFromConfig("title"),
            css=utils.getFileContents(utils.resource_path("./static/style.css")),
            js=utils.getFileContents(utils.resource_path("./static/script.js")),
        ), 200
        
    
    if "uses" in metadata.keys() and metadata['uses'] is not None:
        metadata['uses'] += 1
        database.updateMetadata(shortcode, "uses", metadata['uses'])
        
    try:
        return redirect(url)
    except:
        return utils.URLNotFoundRoute()


def shutdown_server() -> None:
    os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    from main import main
    main()