from flask import Flask, render_template, request
from shoulders import app

@app.route("/", methods=['GET'])
def index():
	return render_template('index.html')