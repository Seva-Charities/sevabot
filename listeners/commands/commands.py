from slack_bolt import BoltResponse, Respond, Ack, Say
import copy
from firebase.firebase import db, firestore

podthai = ["UJM7Z5VGD", "U014KC3E9MF", "U0145C1684V", "U014CUFPNJG", "U01401MQJAJ"]
podtrick = ["UJPDYE4VC", "U0146P6DJQJ", "U0145C1AG1K", "U0146VB99AP", "U014CUFJPC4"]
dadpod = ["UJ9R66SHH", "U01401MPLUE", "U014CUFPARJ"]
kings = ["UJM7Z5VGD", "UJ9R66SHH", "UJPDYE4VC"]
test = ["UJPDYE4VC", "U01CFBL7Z8T"]


def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hello <@{user_id}>!")
    print(user_id)


def notion(body, ack, say):
    ack()
    say("Gathering notion tasks...")


def notify(ack, body, say, command, respond, client):
    ack("notifying...")
    print(body)
    try:
        channel_members = client.conversations_members(channel=body["channel_id"])[
            "members"
        ]
    except:
        channel_members = []
    user = f'<@{body["user_id"]}> has a message for you!'
    if "text" in command:
        if chr(8220) not in command["text"] and '"' not in command["text"]:
            respond(
                text="Error, please use quotation marks to pod and message",
                replace_original=False,
                delete_original=False,
            )
            return
        message = (
            command["text"]
            .strip()
            .replace(chr(8221), '"')
            .replace(chr(8220), '"')
            .split('"')
        )
        message = [x for x in message if x != "" and x != " "]
        pod = message[0]
        text = message[1]
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": user},
            },
            {"type": "divider"},
        ]
        dms = list()
        if pod == "podthai":
            for x in podthai:
                if x not in channel_members:
                    dms.append(x)
            people = " ".join(["<@" + x + ">" for x in podthai])
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": people}}
            )
        elif pod == "podtrick":
            for x in podtrick:
                if x not in channel_members:
                    dms.append(x)
            people = " ".join(["<@" + x + ">" for x in podtrick])
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": people}}
            )
        elif pod == "dadpod":
            for x in dadpod:
                if x not in channel_members:
                    dms.append(x)
            people = " ".join(["<@" + x + ">" for x in dadpod])
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": people}}
            )
        elif pod == "kings":
            for x in kings:
                if x not in channel_members:
                    dms.append(x)
            people = " ".join(["<@" + x + ">" for x in kings])
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": people}}
            )
        else:
            for x in test:
                if x not in channel_members:
                    dms.append(x)
            people = " ".join(["<@" + x + ">" for x in test])
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": people}}
            )
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})
        say(blocks=blocks, text=f"`{command['text']}`")
        blocks = [blocks[0], blocks[-1]]
        for x in dms:
            res = client.conversations_open(users=x)
            channel_id = res["channel"]["id"]
            res = client.chat_postMessage(channel=channel_id, blocks=blocks)


def poll(ack, body, say, command, respond):
    ack()
    user_id = body["user_id"]
    convert = [
        ":zero:",
        ":one:",
        ":two:",
        ":three:",
        ":four:",
        ":five:",
        ":six:",
        ":seven:",
        ":eight:",
        ":nine:",
    ]
    if "text" in command:
        if chr(8220) not in command["text"] and '"' not in command["text"]:
            respond(
                text="Error, please use quotation marks to separate each item!",
                replace_original=False,
                delete_original=False,
            )
            return
        message = (
            command["text"].replace(chr(8221), '"').replace(chr(8220), '"').split('"')
        )
        message = [x for x in message if x != "" and x != " "]
        question = message[0]
        options = message[1:]

        block_template = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "", "verbatim": False},
            "accessory": {
                "type": "button",
                "action_id": "vote",
                "text": {"type": "plain_text", "text": "", "emoji": True},
            },
        }
        blocks = [
            {
                "type": "section",
                # "block_id": "poll-9c223f52-1e8d-4c85-974f-9b6ed21e395e-title-and-menu",
                "text": {"type": "mrkdwn", "text": question, "verbatim": False},
                "accessory": {
                    "type": "overflow",
                    "action_id": "title-and-menu",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":information_source: View info",
                                "emoji": True,
                            },
                            "value": "view_info",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":pushpin: Capture Decision from Poll",
                                "emoji": True,
                            },
                            "value": "capture_decision_from_poll",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":x: Delete Poll",
                                "emoji": True,
                            },
                            "value": "delete_poll",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":house: Go to App Home",
                                "emoji": True,
                            },
                            "value": "go_to_app_home",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": ":bar_chart: Create new Poll",
                                "emoji": True,
                            },
                            "value": "create_new_poll",
                        },
                    ],
                },
            }
        ]
        for i in range(len(options)):
            curr = copy.deepcopy(block_template)
            curr["text"]["text"] = options[i] + "\n"
            num_str = ""
            num = i + 1
            while num > 0:
                num_str = convert[num % 10] + num_str
                num //= 10
            curr["accessory"]["text"]["text"] = num_str
            blocks.append(curr)
        blocks.append(
            {
                "type": "context",
                # "block_id": "nSR",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Created by <@" + command["user_id"] + "> with /poll",
                        "verbatim": False,
                    }
                ],
            }
        )
        print(blocks)
        say(blocks=blocks, text=f"`{command['text']}`")


def vote(ack, body, respond, action, say):
    ack()

    user = body["user"]["id"]
    blocks = body["message"]["blocks"]
    for block in blocks:
        if block["block_id"] == action["block_id"]:
            break
    if user not in block["text"]["text"]:
        block["text"]["text"] += "<@" + user + ">\n"
    else:
        votes = block["text"]["text"]
        block["text"]["text"] = (
            votes[0 : votes.find(user) - 2] + votes[votes.find(user) + len(user) + 1 :]
        )

    # say(f"You selected <@{action['text']['text']}>")
    respond(blocks=blocks, replace_original=True, delete_original=False)


def title_menu(ack, say, body):
    ack()
    say("Request approved 👍")


def wordle(ack, say, body):
    ack()
    wordle_ref = db.collection("sevabot-wordle")
    query = wordle_ref.order_by("number", direction=firestore.Query.DESCENDING).limit(1)
    document = query.get()[0].to_dict()
    number = document["number"]
    scores = document["scores"]
    scores = sorted(scores, key=lambda x: x["score"])
    blocks = build_leaderboard(number, scores)
    say(blocks=blocks)


def build_leaderboard(number, scores):
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Wordle Leaderboard for {number}"},
        },
        {"type": "divider"},
    ]
    score_txt = {"type": "section", "text": {"type": "mrkdwn", "text": "Neil 3/5"}}

    for s in scores:
        cp = copy.deepcopy(score_txt)
        cp["text"]["text"] = f"{s['name']} - {s['score']}/6"
        blocks.append(cp)

    return blocks
