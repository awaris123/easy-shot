# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, jsonify
from Classifier import Classifier
import json
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



@app.route("/sms")
def generateSMS():
   
    body = request.values.get('Body', None)
    if not body:
        body = request.json['query']
        cat = Classifier(body).classify()
        return jsonify(resp=cat)

    cat = Classifier(body).classify()

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message(cat)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)


