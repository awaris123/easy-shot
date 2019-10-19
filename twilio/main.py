# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from flask import Flask
app = Flask(__name__)

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4a171ebb76aac736dce2958d1ffeabd4'
auth_token = '8d3af93e4c6ccffc94360c3fd7cc5566'
client = Client(account_sid, auth_token)



@app.route("/sms")
def hello():
    message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+13368021545',
                     to='+16309911662'
                 )
    print(message.sid) 


    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)


