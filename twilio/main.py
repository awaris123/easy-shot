from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, jsonify
from NLPClassifier import NLPClassifier as Classifier
# from Classifier import Classifier
from Address import Address
from Request import Request
from VoiceQuery import VoiceQuery
import json
import datetime
app = Flask(__name__)


keys = {}
with open('keys.json', 'r') as f:
    keys = json.load(f)

account_sid =keys['account_sid']
auth_token = keys['auth_token']
client = Client(account_sid, auth_token)


def _process(address):
    print("location: ", address)

def isAddress(address):
    for i in  address:
        try:
            int(i)
            return True
        except:
            pass
    return False

msg_cache = {}
@app.route("/sms", methods=['POST'])
def generateSMS():

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    BODY = str(request.values.get('Body', None))
    PHONE_NUMBER = str(request.values.get('From'))
    CATEGORY = Classifier(BODY).classify()
    TIMESTAMP = datetime.date.today()
    print(PHONE_NUMBER, CATEGORY, TIMESTAMP)


    if isAddress(BODY):
        # Handle address case
        address = Address(loc=BODY,ts=TIMESTAMP, num=PHONE_NUMBER)
        if PHONE_NUMBER in msg_cache:
            _process(address.address)
            msg_cache[PHONE_NUMBER].s_loc = address.address
            print("number", PHONE_NUMBER)
            resp.message('Please follow the link')
            resp.message('http://ec2-18-216-217-61.us-east-2.compute.amazonaws.com:3000/'+(PHONE_NUMBER[1::]))
        else:
            resp.message('Please make a request before you enter your address')

    else:
        # handle request case
        if BODY == 'RESTART':
            try:
                del[msg_cache[PHONE_NUMBER]]
                resp.message("If you are still in need of medical assistance, please make a new request")

            except:
                resp.message("You have no pending requests, if you are in need of medical assistance, please make a request")

        elif PHONE_NUMBER in msg_cache:
            resp.message('You already have a pending request, please enter a location or "RESTART" to cancel your request')
        else:
            if CATEGORY == "flu" or CATEGORY == "drug":
                req = Request(cat=CATEGORY, ts=TIMESTAMP, num=PHONE_NUMBER)
                msg_cache[PHONE_NUMBER] = req
                resp.message('Please enter your location')

            elif CATEGORY == "mental":
                resp.message('''Hang in there, it's okay to feel the way you do, sometimes it helps to talk, here is a number to call when you feel this way: 1-800-273-8255''')
                pass

            else:
                resp.message("Your request could not be processed, please rephrase, or consult another service")
                try:
                    del[msg_cache[PHONE_NUMBER]]
                except:
                    pass



    return str(resp)

@app.route("/react", methods =['GET'])
def getSID():
    print("I got here")
    print(request.args['tid'])

    for k in msg_cache.keys():
        print(msg_cache[k].number)
        if (msg_cache[k].number)[1::] == request.args['tid']:

            return jsonify(start=msg_cache[k].s_loc, end="151 N State St Fl 1s")

    return "NONE"


@app.route("/echo", methods =['POST'])
def generateRESP():

    BODY = str(request.values.get('body'))

    LOCATION = request.values.get('loc')
    CATEGORY = Classifier(BODY).classify()
    print(CATEGORY)
    TIMESTAMP = datetime.date.today()
    vc = VoiceQuery(CATEGORY,LOCATION,"")

    ret = ""

    if CATEGORY == "mental":
        ret = "Hang in there, it's okay to feel the way you do, sometimes it helps to talk, here is a number to call when you feel this way: 1-800-273-8255"
    elif CATEGORY == "drug" or CATEGORY == "flu":
        ret = "We are processing your request"
    else:
        ret = "We could not process that request, please try again"
    return jsonify(response=ret)









if __name__ == "__main__":
    app.run(debug=True)
