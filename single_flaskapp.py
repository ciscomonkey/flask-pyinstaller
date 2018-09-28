#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from flask import Flask, render_template

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)


app.run()
