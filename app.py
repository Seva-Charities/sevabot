from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import dotenv
import logging
import os

from slack_bolt import App

from listeners.listeners import register_listeners


dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = App()
register_listeners(app)

podthai = ["UJM7Z5VGD", "U014KC3E9MF", "U0145C1684V", "U014CUFPNJG", "U01401MQJAJ"]
podtrick = ["UJPDYE4VC", "U0146P6DJQJ", "U0145C1AG1K", "U0146VB99AP", "U014CUFJPC4"]
dadpod = ["UJ9R66SHH", "U01401MPLUE", "U014CUFPARJ"]
kings = ["UJM7Z5VGD", "UJ9R66SHH", "UJPDYE4VC"]
test = ["UJPDYE4VC", "U01CFBL7Z8T"]


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if os.environ.get("ENV") == "development":
    app.start(port=3000)
