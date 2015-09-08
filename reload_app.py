#!/usr/bin/env python3

from robobrowser import RoboBrowser
import getpass
import os

url_login = 'https://www.pythonanywhere.com/login/'
url_web_app = 'https://www.pythonanywhere.com/user/ticapix/webapps/#tab_id_ticapix_pythonanywhere_com'

def reload_pyanywhr_app(username=None, password=None):
    if username is None:
        username = raw_input('Username: ')
    if password is None:
        password = getpass.getpass('Password: ')

    browser = RoboBrowser()
    browser.open(url_login)
    assert browser.response.status_code == 200
    browser.session.headers['Referer'] = url_login
    form = browser.get_forms()[0]
    form['username'].value = username
    form['password'].value = password
    browser.submit_form(form)
    assert browser.response.status_code == 200
    browser.open(url_web_app)
    assert browser.response.status_code == 200
    assert browser.url == url_web_app
    form = browser.get_forms(class_='reload_web_app')[0]
    browser.submit_form(form)
    assert browser.response.status_code == 200
    return browser.response.text
    
if __name__ == '__main__':
    reload_app(os.environ['USER'], os.environ['PASS'])
