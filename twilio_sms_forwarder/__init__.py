import configparser
import os

from flask import Flask

from twilio.rest import TwilioRestClient

app = Flask(__name__, static_folder = None)

APP_NAME = 'sms-forwarder'

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

account_sid = config['default']['twilio_account_sid']
auth_token = config['default']['twilio_auth_token']


@app.route('/test')
def hello_twilio():
    client = TwilioRestClient(account_sid, auth_token)
    to = config['default']['forward_to_number']
    from_ = config['default']['forward_to_number']
    message = client.messages.create(to=to, from_=from_, body='test ok!')
    print(message)
