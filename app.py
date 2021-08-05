from flask import render_template, Flask, request, redirect, url_for,\
 send_from_directory, make_response, send_file, Response
from jinja2 import Environment, FileSystemLoader
import config
import astroph
import os

app = Flask(__name__)

env = Environment(loader=FileSystemLoader('templates'),
                  extensions=['jinja2.ext.autoescape'])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
def hello():
    return env.get_template('main.html').render(body=astroph.doit())


if __name__ == "__main__":
    app.run(debug=config.debug)
