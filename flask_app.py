#!/usr/bin/env python3

import os
import glob
import importlib

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask, jsonify, redirect, url_for



rootpath = os.path.abspath(os.path.dirname(__file__))
services = {}

def list_services(rootpath):
    modules = glob.glob(os.path.join(rootpath, '*', '__init__.py'))
    for module_path in [os.path.dirname(module) for module in modules]:
        module_name = os.path.basename(module_path)
        yield (module_name, importlib.import_module(module_name))

app_frontend = Flask(__name__, static_folder = None)
app_frontend.debug = True
apps_backend = [(module, module.APP_NAME, module.app) for (name, module) in list_services(rootpath)]

app = DispatcherMiddleware(app_frontend, dict([(app_name, app) for (_, app_name, app) in apps_backend]))


@app_frontend.route('/')
def index():
    return redirect(url_for('get_services'))


@app_frontend.route('/services')
def get_services():
    services['root'] = {'module': __name__,
                        'rules': [rule.rule for rule in app_frontend.url_map.iter_rules()]}
    for (mod, app_name, app) in apps_backend:
        service = {'module': mod.__name__,
                   'rules': [rule.rule for rule in app.url_map.iter_rules()]}
        services[app_name] = service
    return jsonify({'services': services})

if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)
