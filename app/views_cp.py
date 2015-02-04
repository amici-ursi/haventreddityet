from flask import render_template, request, jsonify
from a_Model import Modelit
from app import app
import networkx as nx
import pickle

pfile = open('graph.pkl','rd')
graph = nx.Graph(pickle.load(pfile))
pfile.close()

@app.route('/')
@app.route('/index')
def index():
 return render_template("subgraph.html", jsonfile = '/static/js/json/default.json')

@app.route('/input')
def subreddits_input():
  return render_template("subgraph.html",jsonfile ='/static/js/json/default.json')

@app.route('/output')
def subreddits_output():
  #pull 'ID' from input field and store it
  sub = request.args.get('ID')
  result = Modelit(G = graph, subreddit = sub)
  return render_template('subgraph.html', jsonfile=result)
