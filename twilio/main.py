# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, jsonify
from Classifier import Classifier
from Address import Address
from Request import Request
import json
import datetime
app = Flask(__name__)


keys = {}
with open('keys.json', 'r') as f:
    keys = json.load(f)

#key = keys[0]

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid =keys['account_sid']
auth_token = keys['auth_token']
client = Client(account_sid, auth_token)

msg_cache = {}

def _process(address):
    print(address)

def isAddress(address):
    for i in  address:
        try:
            int(i)
            return True
        except:
            pass
    return False


@app.route("/sms", methods=['POST'])
def generateSMS():

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    BODY = request.values.get('Body', None)
    PHONE_NUMBER = request.values.get('_from',None)
    CATEGORY = Classifier(BODY).classify()
    TIMESTAMP = datetime.date.today()


    if isAddress(BODY):
        # Handle address case
        address = Address(loc=BODY,ts=TIMESTAMP, num=PHONE_NUMBER)
        if PHONE_NUMBER in msg_cache:
            _process(address.address)
            resp.message('We are processing your request')
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
            if CATEGORY != "neither":
                req = Request(cat=CATEGORY, ts=TIMESTAMP, num=PHONE_NUMBER)
                msg_cache[PHONE_NUMBER] = req
                resp.message('Please enter your location')
            else:
                resp.message("Your request could not be processed, please rephrase, or consult another service")
                try:
                    del[msg_cache[PHONE_NUMBER]]
                except:
                    pass



    return str(resp)


voice_cache = {}
@app.route("/echo", methods =['POST'])
def generateRESP():

    BODY = request.json['body']
    LOCATION = request.json['loc']
    SKILL = request.json['skill']
    CATEGORY = Classifier(body).classify()
    TIMESTAMP = datetime.date.today()
    vc = VoiceQuery(CATEGORY,LOCATION,SKILL)

    if vc.isSkill():
        return jsonify(response=vc.query)

    return jsonify(reponse="None")







if __name__ == "__main__":
    app.run(debug=True)
