import pickle
import networkx as nx

with open("/Users/viegas/Desktop/threads/nx_spanish_tree", "rb") as f:
    u = pickle._Unpickler(f)
    u.encoding = 'bytes'
    g = u.load()

nx.write_gpickle(g, "/Users/viegas/Desktop/threads/nx_spanish_tree_2")