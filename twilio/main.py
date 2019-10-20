# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, jsonify
app = Flask(__name__)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4a171ebb76aac736dce2958d1ffeabd4'
auth_token = '8d3af93e4c6ccffc94360c3fd7cc5566'
client = Client(account_sid, auth_token)



@app.route("/sms")
def generateSMS():
   
    body = request.values.get('Body', None)
    if not body:
        body = request.json['query']
        return jsonify(resp=body)



    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message(body)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)


