from slack_bolt import BoltResponse, Respond, Ack, Say

from firebase.firebase import db, firestore

podthai = ["UJM7Z5VGD", "U014KC3E9MF", "U0145C1684V", "U014CUFPNJG", "U01401MQJAJ"]
podtrick = ["UJPDYE4VC", "U0146P6DJQJ", "U0145C1AG1K", "U0146VB99AP", "U014CUFJPC4"]
dadpod = ["UJ9R66SHH", "U01401MPLUE", "U014CUFPARJ"]
kings = ["UJM7Z5VGD", "UJ9R66SHH", "UJPDYE4VC"]
test = ["UJPDYE4VC", "U01CFBL7Z8T"]

# @ app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    print("hi")
    say(f"Hello there <@{message['user']}>!")


def message_podthai(message, say):
    people = " ".join(["<@" + x + ">" for x in podthai])
    say(people)


def message_podtrick(message, say):
    people = " ".join(["<@" + x + ">" for x in podtrick])
    say(people)


def message_dadpod(message, say):
    people = " ".join(["<@" + x + ">" for x in dadpod])
    say(people)


def message_kings(message, say):
    people = " ".join(["<@" + x + ">" for x in kings])
    say(people)


def react_seva(message, say, client, context):
    print(f"context: {context}")
    print(f"message: {message}")
    res = client.reactions_add(
        channel=context["channel_id"], name="seva", timestamp=message["event_ts"]
    )
    print(f"res: {res}")


def message_wordle(message, say):
    number, score = message["text"].split("\n")[0].split(" ")[1:]
    number = int(number)
    score = int(score[0])
    user = f"<@{message['user']}>"

    say(f"<@{message['user']}> has a wordle score of {score}/6 for {number}")

    # store data in firebase

    # sevabot-wordle

    obj_ref = db.collection("sevabot-wordle").document(str(number))

    if obj_ref.get().to_dict() is None:
        obj_ref.set({"number": number, "scores": []})

    obj_ref.update(
        {
            "number": number,
            "scores": firestore.ArrayUnion([{"name": user, "score": score}]),
        }
    )

    # sevabot-wordle-users
    users_ref = db.collection("sevabot-wordle-users").document(user)
    average = 0
    count = 0
    if users_ref.get().to_dict() is None:
        users_ref.set({"id": user, "count": 0, "average": 0, "scores": []})
    else:
        average = users_ref.get().to_dict()["average"]
        count = users_ref.get().to_dict()["count"]

    new_average = (
        sum(x["score"] for x in users_ref.get().to_dict()["scores"]) + score
    ) / (count + 1)

    users_ref.update(
        {
            "count": users_ref.get().to_dict()["count"] + 1,
            "scores": firestore.ArrayUnion([{"number": number, "score": score}]),
            "average": new_average,
        }
    )
