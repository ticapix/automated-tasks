#!/usr/bin/env python3

import os
import glob
import importlib

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask



rootpath = os.path.abspath(os.path.dirname(__file__))
services = {}

def list_services(rootpath):
    modules = glob.glob(os.path.join(rootpath, '*', '__init__.py'))
    for module_path in [os.path.dirname(module) for module in modules]:
        module_name = os.path.basename(module_path)
        yield (module_name, importlib.import_module(module_name))

app_frontend = Flask(__name__)
app_frontend.debug = True
apps_backend = [(name, module.app) for (name, module) in list_services(rootpath)]

app = DispatcherMiddleware(app_frontend, dict(apps_backend))


@app_frontend.route('/')
def hello_world():
    return 'Hello from Flask!'


@app_frontend.route('/process-email')
def process_email():
    return "Hello World!"

if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)
