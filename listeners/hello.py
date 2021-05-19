from app import app


# Listens to incoming messages that contain "hello"


@ app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    print('hi')
    say(f"Hello there <@{message['user']}>!")