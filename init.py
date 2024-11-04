import os
import json

config = {
    "title": "URL Shortener",
    "version": "1.0",
}

def initConfig():
    if os.path.exists("./config.json"):
        d = json.loads(open("./config.json").read())
        for i in d: config[i] = d[i]
        with open("./config.json", "w") as f:
            json.dump(config, f, indent="\t")
    else:
        openfile=open("./config.json", "w")
        d = {}
        for i in d: config[i] = d[i]
        openfile.write(json.dumps(config, indent="\t"))
        openfile.close()
        
