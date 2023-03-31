import networkx as nx
import angr
from itertools import pairwise
import os

def clear_images_directory():
    dir_name = 'images'
    directory = os.listdir(dir_name)
    for item in directory:
        if item.endswith(".png"):
            os.remove(os.path.join(dir_name, item))

def build_node_dict(cfg):
    node_dict = {}
    nodes = [node for node in cfg.nodes()]
    for index,node in enumerate(nodes):   
        node_dict[index] = node
    return node_dict

def detectLoops(fp):
    p = angr.Project(fp, auto_load_libs=False)
    # Gets the symbol for main.
    main = p.loader.main_object.get_symbol("main")
    # Gets starting address to form the cfg
    start_state = p.factory.blank_state(addr=main.rebased_addr)
    # Creates cfg of the main function, but does not pull anything but the blocks.
    cfg = p.analyses.CFGEmulated(fail_fast=True, starts=[main.rebased_addr], initial_state=start_state)
    # Creates a local copy of the node list.
    nodeDict = build_node_dict(cfg.graph)
    # Creates the dominance frontier which I will use to iterate over each nodes dominators.
    dom_front = list(nx.dominance.dominance_frontiers(cfg.graph, nodeDict[0]).items())

    # Creates the lists to store the various paths.
    RemoveEdgeList = []
    NaturalLoopPathList = []
    # Inside the dom front there is a list of tuples of the form: (Node, [Dominator List]).
    # This allows me to iterate through both the nodes and their respective dominators in a clean fashion.
    for node_dom_tuple in dom_front:
        header_node = node_dom_tuple[0]
        dom_list = node_dom_tuple[1]
        for dom in dom_list:
            # Using networkx I fetched all the paths from the dominator to the header node.
            paths = nx.all_simple_paths(cfg.graph, dom, header_node)
            
            for path in paths:
                # I decided to keep all of the paths that arent loops for future use.
                if header_node not in path:
                    RemoveEdgeList.append(path)
                # Stores all the loops into a list for filtering.
                if path[0] == dom and path[-1] == header_node and path[0] in path[-1].successors:
                    NaturalLoopPathList.append(path)
    # Due to the nature of the algorithm I used it returns all of the configurations of the loop.
    # In the next section I sort and filter the list so that the header nodes with the highest in_degree are left.
    NaturalLoopPathList.sort(key=lambda x: cfg.graph.degree(x[0]))
    NaturalLoopPathList.reverse()
    output_paths = []
    for path in NaturalLoopPathList:
        if path[0] == NaturalLoopPathList[0][0]:
            path.append(path[0])
            output_paths.append(path)
    
    # This just flips all edges stored in the path of the loop to red and does this for all loops found within the cfg.
    for index,path in enumerate(output_paths):
        graph_copy = cfg.graph.copy()
        pairwise_list = pairwise(path)
        for pw in pairwise_list:
            a,b = pw
            for e in graph_copy.edges():
                if e[0] == a and e[1] == b:
                    graph_copy[e[0]][e[1]]['color'] = 'red'
        A = nx.nx_agraph.to_agraph(graph_copy)
        A.layout(prog='dot')
        A.draw(f'images/Loop{index}.png')

# Generates a dom tree. This was mostly for understanding.
# entry_node = cfg.get_any_node(main.rebased_addr)
# dom_tree = build_dominator_tree(cfg.graph, entry_node)
# A = nx.nx_agraph.to_agraph(dom_tree)
# A.layout(prog='dot')
# A.draw('domtree.png')

# def build_dominator_tree(cfg, entry_node):
# # Initialize the dominator of each node to be the set of all nodes
# dom = {node: set(cfg.nodes()) for node in cfg.nodes()}

# # The entry node dominates only itself
# dom[entry_node] = set([entry_node])

# changed = True
# while changed:
#     changed = False
#     for node in cfg.nodes():
#         new_dom = set([node]).union(
#             *[dom[pred] for pred in cfg.predecessors(node)])
#         if new_dom != dom[node]:
#             changed = True
#             dom[node] = new_dom
            
# return nx.bfs_tree(cfg.reverse(), entry_node, dom)

