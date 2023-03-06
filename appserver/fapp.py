# Import the flask library
from flask import Flask, request
from sonos_manager import get_sonos_manager

# create the flask application object pa
app = Flask(__name__)

sonos = get_sonos_manager()

## Decorator making the subsequent function a route
@app.route("/", methods=["GET"])
## this functions return value is the response of the route (function name doesn't matter)
def first_route():
  return "hello world", 200 ## will return text with a 200 status

@app.route("/playlists", methods=["GET"] )
def playlists():
    return {"playlists":sonos.get_playlists()},200

@app.route("/selectp", methods=["POST"] )
def selectp():
    if request.method == "POST":
        body = request.json
        return body, 200

@app.route("/select/<id>", methods=["GET"] )
def select(id):
    sonos.select(id),200
    return {},200

@app.route("/playpause", methods=["GET"] )
def playpause():
    sonos.play_pause(),200
    return {},200

@app.route("/next", methods=["GET"] )
def next():
    sonos.next(),200
    return {},200

@app.route("/prev", methods=["GET"] )
def prev():
    sonos.previous(),200
    return {},200

@app.route("/playstatus", methods=["GET"] )
def playstatus():
    return sonos.play_status(),200

@app.route("/info", methods=["GET"] )
def info():
    return sonos.info(),200

@app.route("/volup", methods=["GET"] )
def volup():
    sonos.vol_up(2)
    return {},200

@app.route("/voldown", methods=["GET"] )
def voldown():
    sonos.vol_down(-5)
    return {},200
