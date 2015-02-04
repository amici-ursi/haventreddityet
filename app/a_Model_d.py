from operator import itemgetter
from networkx.readwrite import json_graph
import networkx as nx
import pickle
import json

def get_neighbors(G, current_node, it, max_its = 3, max_edges = 10):

    nodes = set()
    nodes.add(current_node)
    if it >= max_its:
        return nodes

    #Get list of neighbors and edge weight. Sort by weight
    neighbors = [ (neighbor, G[current_node][neighbor]['weight']/float(len(G.neighbors(neighbor)))) for neighbor in G.neighbors(current_node)]
    neighbors = sorted(neighbors, key=itemgetter(1))

    #Add top nodes and edges to lists
    for k in range(min(max_edges,len(neighbors))):
        nodes.add(neighbors[k][0])
        k += 1

    #get neighbors of neighbors 
    it += 1
    for n in nodes:
        nodes = nodes.union(get_neighbors(G,n,it,max_its,max(1,int(max_edges/3))))

    return nodes

def Modelit(subreddit):

    node_name = subreddit #starting node
    n_neighborhoods = 2 # number of neighborhoods to consider
    max_nodes = 100 #max number of nodes for a subgraph
    edge_limit = 3 #max number of edges for a node

    #open graph, previously saved as a pickle object
    pfile = open('/Users/James/python/insight/project/data/graph.pkl','rd')
    G = nx.Graph(pickle.load(pfile))
    pfile.close()

    #find the starting node
    start_node = -1
    for n in G:
        if G.node[n]['label']==node_name:
            start_node = n
            break

    #get neighbors and make subgraph
    neighbors = get_neighbors(G, start_node , 0, n_neighborhoods, 10)
    subG = G.subgraph(neighbors)

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
   
