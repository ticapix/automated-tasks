from flask import Flask, jsonify

from twilio.rest import TwilioRestClient
from twilio import twiml

from config import config

APP_NAME = 'sms-forwarder'

app = Flask(__name__, static_folder = None)

account_sid = config['twilio']['account_sid']
auth_token = config['twilio']['auth_token']


@app.route('/test')
def test():
    client = TwilioRestClient(account_sid, auth_token)
    to = config['twilio']['to_number']
    from_ = config['twilio']['from_number']
    message = client.messages.create(to=to, from_=from_, body='test ok!')
    print(message, dir(message))
    return jsonify({'success': True})


@app.route('/fwcall', methods=['GET', 'POST'])
def forward_call():
    resp = twiml.Response()
    resp.dial(config['twilio']['to_number'])
    resp.say("The call failed, or the remote party hung up. Goodbye.")
    return str(resp)

@app.route('/call_auth', methods=['GET', 'POST'])
def call_auth():
    resp = twiml.Response()
    resp.pause(length=3)
    resp.play(digits=config['twilio']['auth_code'])
    return str(resp)
