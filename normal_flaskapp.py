#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)


app.run()
