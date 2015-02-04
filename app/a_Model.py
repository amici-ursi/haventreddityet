from operator import itemgetter
from networkx.readwrite import json_graph
import numpy as np
import networkx as nx
import pickle
import json
import math

def Modelit(G, subreddit):    
    node_name = subreddit.lower() #starting node
    r_nodes = 6 # number of random steps
    n_iters = 50 #number of random walks
    n_nodes = 100 #max number of nodes for a subgraph
    
    weight_decay = .99
    transit_factor =  0.9

    #find the starting node
    subG = nx.Graph()
    nodes_visited = dict()
    start_node = -1
    for n in G:
        if G.node[n]['label']==node_name:
            start_node = n
            break

    if subreddit == 'notthesubreddityourelookingfor':
    	subG = G.subgraph([start_node]).copy()
    	jsonfile_name = 'static/js/json/' + subreddit + '.json'
    	d = json_graph.node_link_data(subG)
    	json.dump(d, open(jsonfile_name,'wd'))
    	return "/static/js/json/" + str(subreddit) + ".json"   

    #keep track of the number of times each node gets visited
    nodes_visited[start_node] = 1

    #take the path less traveled

    #keep track of the number of links each node has
    edges_for_node = dict()

    #start random walks 
    for j in range(n_iters):

        current_node = start_node

        #keep track of nodes visited
        #trans = set()

        #start random steps
        for i in range(r_nodes):

            #make list of transition probabilities
            links = nx.edges(G,current_node)
            probs = []
            for link in links:
                randn = np.random.random()
                connectivity = math.pow(weight_decay,G.node[link[1]]['degree'])
                if link[1] in nodes_visited:
                    transit_weight = math.pow(transit_factor,nodes_visited[link[1]])
                else:
                    transit_weight = 1. 
                weight = G[link[0]][link[1]]['weight']
                transition_prob = randn*weight*transit_weight*connectivity
                probs.append(transition_prob)

            #move to the node with the highest transition probability
            #keep track of nodes visited 
            #if current_node not in edges_for_node:
            #    edges_for_node[current_node] = dict()

            #find node with largest trans prob
            #while len(probs)>0:
            arg_max_prob = max(enumerate(probs), key=itemgetter(1))[0]
            #    del probs[arg_max_prob]
            next_node = links[arg_max_prob][1]
            #    if (current_node,next_node) not in trans:
            #        break

            #if all transition done then next it:
            #if len(probs)==0:
            #    continue 

            #keep track to transitions (forward and back)
            #trans.add((next_node,current_node))
            #trans.add((current_node,next_node))

            #keep track of the most visited nodes
            if next_node in nodes_visited:
                nodes_visited[next_node] += 1
            else:
                nodes_visited[next_node] = 1
            current_node = next_node

    #Fill subgraph         
    sub_nodes = [start_node]
    del nodes_visited[start_node]
    for k in range(min(n_nodes,len(nodes_visited))):
        top_node = max(nodes_visited.iteritems(), key=itemgetter(1))[0]
        sub_nodes.append(top_node)
        del nodes_visited[top_node]
        
    subG = G.subgraph(sub_nodes).copy()

    #highligh start node
    subG.node[start_node]['cat1'] += 'selected'
    #correct internal node index. So annoying
    start = 0
    subG = nx.convert_node_labels_to_integers(subG,first_label=start)
    
    #correct interanl node links indicies. super annoying 
    i = 0
    for n in subG:
        link_list = []
        eds = nx.edges(subG,n)
        for ed in eds:
            link_list.append(ed[1])
        subG.node[n]['links'] = link_list


    #save file and output file name for D3 to find
    jsonfile_name = 'static/js/json/' + subreddit + '.json'
    d = json_graph.node_link_data(subG)
    json.dump(d, open(jsonfile_name,'wd'))
    return "/static/js/json/" + str(subreddit) + ".json"
   
