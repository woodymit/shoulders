import pickle
import json
import os

from flask import Flask, render_template, request
from shoulders import app

from scrape_scholar import CitationGraph
from scrape_scholar import search_string
from ConvertAListToPoints import convertAListToPoints

slash_index = __file__.rindex('/')
temp_dir = __file__[:slash_index]
temp_file = os.path.join(temp_dir, 'tempfile.txt')


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/search", methods=['POST'])
def search():
    query_string = str(request.form['search_string'])

    paper_list = search_string(query_string, 5)
    with open(temp_file, 'w') as fh:
        pickle.dump(paper_list, fh)

    return json.dumps([p.get_data_dict() for p in paper_list])


@app.route("/graph", methods=['POST'])
def graph():

    # title = str(request.form['title'])
    # height = int(request.form['height'])
    # width = int(request.form['width'])

    # with open(temp_file, 'r') as fh:
    #     paper_list = pickle.load(fh)

    # center_paper = None
    # for paper in paper_list:
    #     if paper.title == title:
    #         center_paper = paper
    #         break

    # graph = CitationGraph(center_paper)
    # graph.expand_newest_edge()

    # import ipdb
    # ipdb.set_trace()

    # json_data = convertAListToPoints(
    #         graph.children, center_paper, width, height)

    with open('json_data_1.txt', 'r') as fh:
        json_data = fh.next()

    return json_data
