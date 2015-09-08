import configparser
import os

from flask import Flask, jsonify

from twilio.rest import TwilioRestClient
from twilio import twiml

app = Flask(__name__, static_folder = None)

APP_NAME = 'sms-forwarder'

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

account_sid = config['default']['account_sid']
auth_token = config['default']['auth_token']


@app.route('/test')
def test():
    client = TwilioRestClient(account_sid, auth_token)
    to = config['default']['to_number']
    from_ = config['default']['from_number']
    message = client.messages.create(to=to, from_=from_, body='test ok!')
    print(message, dir(message))
    return jsonify({'success': True})


@app.route('/fwcall')
def forward_call():
    resp = twiml.Response()
    # Dial (310) 555-1212 - connect that number to the incoming caller.
    resp.dial(config['default']['to_number'])
    # If the dial fails:
    resp.say("The call failed, or the remote party hung up. Goodbye.")
    return str(resp)
