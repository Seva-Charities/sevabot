import re

from listeners.events.events import *
from listeners.commands.commands import *
from listeners.commands.admin import *

from slack_bolt import Ack, App


def register_listeners(app):

    # Events

    app.message("hello")(message_hello)

    app.message("@podthai")(message_podthai)

    app.message("@podtrick")(message_podtrick)

    app.message("@dadpod")(message_dadpod)

    app.message("@kings")(message_kings)

    app.message(re.compile("(seva|Seva|SEVA)"))(react_seva)

    app.message("Wordle")(message_wordle)

    # Commands

    app.command("/hello")(hello)

    app.command("/notify")(notify)

    app.command("/poll")(poll)

    app.command("/notion")(notion)

    app.command("/admin")(ack=admin_ack, lazy=[admin])

    app.command("/wordle")(wordle)

    # Actions

    app.action("vote")(vote)

    app.action("title-and-menu")(title_menu)
