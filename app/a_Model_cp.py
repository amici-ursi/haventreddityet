from operator import itemgetter
from networkx.readwrite import json_graph
import numpy as np
import networkx as nx
import pickle
import json
import math

def Modelit(subreddit):    
    node_name = subreddit #starting node
    r_nodes = 20 # number of random steps 
    n_iters = 500 #number of random walks
    n_nodes = 100 #max number of nodes for a subgraph

    #open graph, previously saved as a pickle object
    pfile = open('/Users/James/python/insight/project/data/graph.pkl','rd')
    G = nx.Graph(pickle.load(pfile))
    pfile.close()

    #find the starting node
    subG = nx.Graph()
    nodes_visited = dict()
    start_node = -1
    for n in G:
        if G.node[n]['label']==node_name:
            start_node = n
            break

    #keep track of the number of times each node gets visited
    nodes_visited[start_node] = 1

    #keep track of the number of links each node has
    edges_for_node = dict()

    #start random walks 
    for j in range(n_iters):

        current_node = start_node

        #start random steps
        for i in range(r_nodes):

            #make list of transition probabilities
            links = nx.edges(G,current_node)
            probs = []
            for link in links:
                randn = np.random.random()
                connectivity = math.pow(float(len(G.neighbors(link[1]))),.7)
                #connectivity = 1.
                weight = G[link[0]][link[1]]['weight']
                transition_prob = randn*weight/connectivity
                probs.append(transition_prob)

            #move to the node with the highest transition probability
            #keep track of nodes visited 
            if current_node not in edges_for_node:
                edges_for_node[current_node] = dict()

            
            arg_max_prob = max(enumerate(probs), key=itemgetter(1))[0]
            next_node = links[arg_max_prob][1]
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
        
    subG = G.subgraph(sub_nodes)


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
    jsonfile_name = '/Users/James/python/insight/project/app/static/js/json/' + subreddit + '.json'
    d = json_graph.node_link_data(subG)
    json.dump(d, open(jsonfile_name,'wd'))
    return "/static/js/json/" + str(subreddit) + ".json"
   
