#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)


URI_ROOT = '/publication-erdf'


@app.route(URI_ROOT + '/process-email')
def process_email():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
