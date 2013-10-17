from flask import render_template, Flask, request, redirect, url_for,\
	send_from_directory, make_response, send_file, Response
from jinja2 import Environment, FileSystemLoader

import astroph

app = Flask(__name__)

env = Environment(loader=FileSystemLoader(
	'templates'), extensions=['jinja2.ext.autoescape'])

@app.route("/")
def hello():
	return env.get_template(
		'main.html').render(body=astroph.doit())
    
if __name__ == "__main__":
	app.run(debug=True)