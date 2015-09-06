import configparser
import os

from flask import Flask
app = Flask(__name__)


def load_config(filepath):
    config = configparser.ConfigParser()
    config.read(filepath)
    return config

# https://docs.python.org/3/library/configparser.html
config = load_config(os.path.join(os.path.dirname(__file__), 'config.ini'))
for section in config.sections():
    for key in config[section].keys():
        print(section + '.' + key + ' = ' + config[section][key])

@app.route('/')
def hello_twilio():
    return 'Hello from Flask!'

a = """
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = "ACXXXXXXXXXXXXXXXXX"
auth_token = "YYYYYYYYYYYYYYYYYY"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+12316851234", from_="+15555555555",
                                     body="Hello there!")
                                     """