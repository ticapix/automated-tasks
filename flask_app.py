#!/usr/bin/env python3

import os
import glob
import importlib

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask, jsonify, redirect, url_for



rootpath = os.path.abspath(os.path.dirname(__file__))

def list_application(rootpath):
    modules = glob.glob(os.path.join(rootpath, '*', '__init__.py'))
    for module_path in [os.path.dirname(module) for module in modules]:
        module_name = os.path.basename(module_path)
        print('module_name', module_name)
        yield (module_name, importlib.import_module(module_name))

app_frontend = Flask(__name__, static_folder = None)
app_frontend.debug = True
services = [module for (_, module) in list_application(rootpath)]
apps_backend = dict([(service.APP_NAME, service.app) for service in services])
app = DispatcherMiddleware(app_frontend, apps_backend)
print(app)

@app_frontend.route('/')
def index():
    return redirect(url_for('list_services'))


@app_frontend.route('/services')
def list_services():
    apis = {'root': {'module': __name__,
                     'rules': [rule.rule for rule in app_frontend.url_map.iter_rules()]}
            }
    for service in services:
        info = {'module': service.__name__,
                'rules': [rule.rule for rule in service.app.url_map.iter_rules()]}
        apis[service.APP_NAME] = info
    return jsonify({'services': apis})


if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)
