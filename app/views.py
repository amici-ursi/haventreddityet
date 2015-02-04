from flask import render_template, request, jsonify
from flask import Flask
import random 
from a_Model import Modelit
import networkx as nx
import pickle

app = Flask(__name__)

#load full graph here (only once!)
pfile = open('graph.pkl','rd')
graph = nx.Graph(pickle.load(pfile))
pfile.close()

#make list of subreddits in graph for random home page
subreddits = [graph.node[n]['label'] for n in graph.nodes() if len(graph.node[n]['links'])>1]

@app.route('/')
@app.route('/index')
def index():
 sub = subreddits[random.randrange(0,len(subreddits))]
 result = Modelit(G = graph, subreddit = sub)
 return render_template("subgraph.html", jsonfile = result)

@app.route('/input')
def subreddits_input():
  sub = subreddits[random.randrange(0,len(subreddits))]
  result = Modelit(G = graph, subreddit = sub)
  return render_template("subgraph.html",jsonfile = result)

@app.route('/output')
def subreddits_output():
  #pull 'ID' from input field and store it
  sub = request.args.get('ID').lower()
  if sub.find('r/') == 0:
	sub = sub[2:]
  if sub not in subreddits:
	sub = 'notthesubreddityourelookingfor'
  result = Modelit(G = graph, subreddit = sub)
  return render_template('subgraph.html', jsonfile=result)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)
