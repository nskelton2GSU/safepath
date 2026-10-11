import sys
import pathlib as Path

sys.path.insert(0, str(Path.Path(__file__).parent.parent))

from graph import load_graph, add_safety_weights, path_coords 
from routes import route

G = load_graph() 
G = add_safety_weights(G) 

path = route(G, 33.7756, -84.3963, 33.7780, -84.3940) 
print("path length (nodes):", len(path)) 
print("first coord:", path_coords(G, path)[0])