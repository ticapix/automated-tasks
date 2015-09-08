#!/usr/bin/env python3

import os
import glob
import importlib
import subprocess
import multiprocessing

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask import Flask, jsonify, redirect, url_for

from reload_app import reload_pyanywhr_app
from config import config, rootpath

# Frontend service
app_frontend = Flask(__name__, static_folder = None)
app_frontend.debug = True

# Backend services
def get_services(rootpath):
    modules = glob.glob(os.path.join(rootpath, '*', '__init__.py'))
    for module_path in [os.path.dirname(module) for module in modules]:
        module_name = os.path.basename(module_path)
        print('module_name', module_name)
        module = importlib.import_module(module_name)
        module.app.debug = True
        yield (module, '/' + module.APP_NAME, module.app)

services = list(get_services(rootpath))

# application dispatcher
app = DispatcherMiddleware(app_frontend, dict([(app_path, app) for (_, app_path, app) in services]))

# routes
@app_frontend.route('/')
def index():
    return redirect(url_for('list_services'))


@app_frontend.route('/services')
def list_services():
    apis = {'': {'module': __name__,
                  'rules': [rule.rule for rule in app_frontend.url_map.iter_rules()]}
            }
    for (module, app_path, app) in services:
        info = {'module': module.__name__,
                'rules': [rule.rule for rule in app.url_map.iter_rules()]}
        apis[app_path] = info
    return jsonify({'services': apis})


@app_frontend.route('/reload', methods=['GET', 'POST'])
def reload_app():
    # TODO git pull
    assert subprocess.call(['git', 'pull'], cwd=rootpath) == 0
    target = reload_pyanywhr_app
    kwargs = {'username': config['default']['pythonanywhere_user'],
              'password': config['default']['pythonanywhere_pass']}
    multiprocessing.Process(name='daemon', target=target, kwargs=kwargs, daemon=True).start()
    return 'OK'


if __name__ == "__main__":
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)
