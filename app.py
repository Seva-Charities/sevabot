from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import dotenv
import logging

from slack_bolt import App

dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)
app = App()


@app.command("/hello")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")

# Listens to incoming messages that contain "hello"


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
