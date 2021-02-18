import os
import dotenv
from slack_bolt import App
import re

# Initializes your app with your bot token and signing secret
dotenv.load_dotenv(dotenv_path='.env')
logging.basicConfig(level=logging.DEBUG)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Listens to incoming messages that contain "hello"


@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.message(re.compile("(seva|Seva)"))
def react_seva(message, say):
    print(message)
    # say(
    #     blocks=[
    #         {
    #             "type": "section",
    #             "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
    #             "accessory": {
    #                 "type": "button",
    #                 "text": {"type": "plain_text", "text": "Click Me"},
    #                 "action_id": "button_click"
    #             }
    #         }
    #     ],
    #     text=f"Hey there <@{message['user']}>!"
    # )


@ app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
