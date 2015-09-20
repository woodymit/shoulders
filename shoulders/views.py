import json

from flask import Flask, render_template, request
from shoulders import app

from scrape_scholar import search_string


@app.route("/", methods=['GET','POST'])
def index():
	return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
	query_string = str(request.form['search_string'])

	paper_list = search_string(query_string, 5)
	return json.dumps([p.get_data_dict() for p in paper_list])
