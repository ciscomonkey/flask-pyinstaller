#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import webbrowser
from threading import Timer
from flask import Flask, render_template

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run()
