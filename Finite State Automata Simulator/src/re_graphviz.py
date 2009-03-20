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

def graph_from_fsa(fsa):
    g = gv.digraph('graph')
    gv.setv(g, 'rankdir', 'LR')
    
    for st in fsa.states():
        n = gv.node(g, str(st))
        gv.setv(n, 'label', str(st))
        
        gv.setv(n, 'shape', ('double' if st in fsa.final_s else '') + 'circle')
        
        if (st == fsa.first_s):
            inv_n = gv.node(g, str(id([])))
            gv.setv(inv_n, 'label', '')
            gv.setv(inv_n, 'style', 'invis')
            gv.setv(gv.edge(inv_n, n), 'color', 'gray51')
    
    for s1, s2, c in fsa.transitions():
        e = gv.edge(g, str(s1), str(s2))
        
        gv.setv(e, 'color', 'gray71')
        gv.setv(e, 'arrowsize', '0.7')
    
        if (c == '#'):
            c = u'\u03bb'
            gv.setv(e, 'fontcolor', 'goldenrod2')
            gv.setv(e, 'style', 'dashed')
        else:
            gv.setv(e, 'fontcolor', 'firebrick2')
            
        gv.setv(e, 'label', (' ' + c + ' ').encode('utf-8'))
    
    return g


def render_parse_tree(tree, filename, same_level = False, output_dot = None):
    g = graph_from_parse_tree(tree, same_level)
    render_graph(g, filename, output_dot)

def render_fsa(fsa, filename, output_dot = None):
    g = graph_from_fsa(fsa)
    render_graph(g, filename, output_dot)

def render_graph(g, filename, output_dot = None):
    gv.setv(g, 'center', 'true')
    gv.setv(g, 'fontname', 'helvetica')
    gv.layout(g, 'dot')
    
    if (output_dot):
        gv.write(g, output_dot)
    
    gv.render(g, 'png', filename) 
