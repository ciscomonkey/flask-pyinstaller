# flask-pyinstaller

Just my notes on creating standalone flask app using pyinstaller for some projects I am working on.

# Setup

```shell
$ git clone https://github.com/ciscomonkey/flask-pyinstaller.git .
$ pip install pyinstaller flask
```

# Normal build command:

```shell
$ pyinstaller --onefile --add-data 'templates:templates' --add-data 'static:static' normal_flaskapp.py
```

# What fails with this?

When you pull up http://localhost:5000/ you'll get a server error and on the console you'll see:

```shell
~/dev/cflask/dist$ ./normal_flaskapp
 * Serving Flask app "normal_flaskapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
[2018-09-28 11:50:02,099] ERROR in app: Exception on / [GET]
Traceback (most recent call last):
  File "site-packages/flask/app.py", line 2292, in wsgi_app
  File "site-packages/flask/app.py", line 1815, in full_dispatch_request
  File "site-packages/flask/app.py", line 1718, in handle_user_exception
  File "site-packages/flask/_compat.py", line 35, in reraise
  File "site-packages/flask/app.py", line 1813, in full_dispatch_request
  File "site-packages/flask/app.py", line 1799, in dispatch_request
  File "normal_flaskapp.py", line 12, in hello_world
  File "site-packages/flask/templating.py", line 134, in render_template
  File "site-packages/jinja2/environment.py", line 869, in get_or_select_template
  File "site-packages/jinja2/environment.py", line 830, in get_template
  File "site-packages/jinja2/environment.py", line 804, in _load_template
  File "site-packages/jinja2/loaders.py", line 113, in load
  File "site-packages/flask/templating.py", line 58, in get_source
  File "site-packages/flask/templating.py", line 86, in _get_source_fast
jinja2.exceptions.TemplateNotFound: hello.html
```
Don't run it as ```./build/normal_flaskapp``` as this puts the templates folder in the relative path where Flask expects to see them. When you distribute your standalone executable, those folders won't be there and you'll see the error from above.

# How to fix?

The problem is that when the site is running in packaged form, the templates are inside
a directory called _MEIxxxxxx under the temp directory (see https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#using-file) and you have to tell Flask about this.

To do this use the template_folder argument (see http://flask.pocoo.org/docs/1.0/api/#application-object).

Finally, the if clause is there to ensure that we can still use it unpackaged during development.

This is in ```single_flaskapp.py```

```python
import os
import sys
from flask import Flask

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
```

Now when we run:

```shell
~/dev/cflask/dist$ ./single_flaskapp
 * Serving Flask app "single_flaskapp" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [28/Sep/2018 11:45:36] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [28/Sep/2018 11:45:36] "GET /favicon.ico HTTP/1.1" 200 -
```
