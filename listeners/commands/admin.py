from slack_bolt import BoltResponse, Respond, Ack, Say

import sys
import copy
import json

sys.path.insert(1,'../../')

from firebase.firebase import db

podthai = ["UJM7Z5VGD", "U014KC3E9MF", "U0145C1684V", "U014CUFPNJG", "U01401MQJAJ"]
podtrick = ["UJPDYE4VC", "U0146P6DJQJ", "U0145C1AG1K", "U0146VB99AP", "U014CUFJPC4"]
dadpod = ["UJ9R66SHH", "U01401MPLUE", "U014CUFPARJ"]
kings = ["UJM7Z5VGD", "UJ9R66SHH", "UJPDYE4VC"]
test = ["UJPDYE4VC", "U01CFBL7Z8T"]


def admin_ack(ack, body):
    ack()
    print(body)

def admin(ack, body, say, command, respond, client):
    admins = db.collection('sevabot-groups').document('admin').get().to_dict()
    print(admins)
    user_id = body['user_id']
    if user_id not in admins['users']:
        say('Sorry, you are not an admin!')

    f = open('users.json', 'w')
    users = client.users_list()
    json.dump(str(users), f)
    f.close()

