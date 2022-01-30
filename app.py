from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import dotenv
import logging
import os

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.response import BoltResponse

from listeners.listeners import register_listeners

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)


def success(args: SuccessArgs) -> BoltResponse:
    assert args.request is not None
    return BoltResponse(
        status=200,  # you can redirect users too
        body="Your own response to end-users here",
    )


def failure(args: FailureArgs) -> BoltResponse:
    assert args.request is not None
    assert args.reason is not None
    return BoltResponse(
        status=args.suggested_status_code, body="Your own response to end-users here"
    )


callback_options = CallbackOptions(success=success, failure=failure)

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=[
        "channels:history",
        "channels:join",
        "channels:manage",
        "channels:read",
        "chat:write",
        "commands",
        "emoji:write",
        "groups:history",
        "groups:read",
        "im:history",
        "im:read",
        "im:write",
        "incoming-webhook",
        "mpim:history",
        "mpim:read",
        "mpim:write",
        "reactions:write",
        "users:read",
    ],
    user_scopes=[],
    redirect_uri=None,
    install_path="/slack/install",
    redirect_uri_path="/slack/oauth_redirect",
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states"),
    callback_options=callback_options,
    installation_store=FileInstallationStore(base_dir="./data/installations"),
)

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"], oauth_settings=oauth_settings
)
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
    print("hello")
    return handler.handle(request)


@flask_app.route("/hello", methods=["POST"])
def hello():
    print("HELP")
    return "Hello World"


if os.environ.get("ENV") == "development":
    app.start(port=3000)
