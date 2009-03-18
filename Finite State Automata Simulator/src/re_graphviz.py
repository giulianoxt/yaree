"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - GraphViz related routines
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


import gv
from re_parser import Rule


def graph_from_parse_tree(root, same_level = False):
    def visit(node, graph, subgraph):
        if isinstance(node, Rule):
            gnode = gv.node(graph, str(id(node)))
            stylize_rule(gnode, node)
            
            for n in node.childs:
                visit(n, graph, subgraph)
                e = gv.edge(graph, str(id(node)), str(id(n)))
                stylize_edge(e)
        else: # Token
            gnode = gv.node(subgraph, str(id(node)))
            stylize_token(gnode, node)

    g = gv.digraph('graph')
    tg = gv.graph(g, 'token_graph')
    
    if (same_level):
        gv.setv(tg, 'rank', 'same')
        
    visit(root, g, tg)
    return g

def stylize_rule(rnode, node):
    gv.setv(rnode, 'label', node.name)
    gv.setv(rnode, 'style', 'bold')

def stylize_token(tnode, node):
    gv.setv(tnode, 'label', node.lexem)
    gv.setv(tnode, 'shape', 'rect')
    gv.setv(tnode, 'width', '0.5')
    gv.setv(tnode, 'regular', 'true')
    gv.setv(tnode, 'fixedsize', 'true')
    gv.setv(tnode, 'color', 'gray51')
    gv.setv(tnode, 'fontcolor', 'firebrick2')

def stylize_edge(edge):
    gv.setv(edge, 'arrowhead', 'diamond')
    gv.setv(edge, 'arrowsize', '0.35')

def render_parse_tree(tree, filename, same_level = False, output_dot = None):
    g = graph_from_parse_tree(tree, same_level)
    gv.setv(g, 'center', 'true')
    gv.setv(g, 'fontname', 'helvetica')
    gv.layout(g, 'dot')
    
    if (output_dot):
        gv.write(g, output_dot)
    
    gv.render(g, 'png', filename)
