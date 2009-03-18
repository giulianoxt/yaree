"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - Main executable script
  
  Usage:
    
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


import sys
from random import choice
from getopt import getopt

from re_parser import RegExpParser
from re_graphviz import render_parse_tree


sample_re = ['((a.b*.c) + d.e*)', '((a.b.c + #) + d.e*)', '(a + b)*.c + d*']


if __name__ == '__main__':
    r = None
    render_ptree = None
    same_rank = False
    output_dot = None
    
    opts, _ = getopt(sys.argv[1:], '',
        ['auto', 'same-level', 'render-ptree=', 'out-dot='])

    for (arg, val) in opts:
        if (arg == '--auto'):
            r = choice(sample_re)
        elif (arg == '--render-ptree'):
            render_ptree = val
        elif (arg == '--same-level'):
            same_rank = True
        elif (arg == '--out-dot'):
            output_dot = val
    
    if (r is None):
        r = raw_input('Enter a regular expression: ')
    
    tree = RegExpParser(r).parse()
    
    if (render_ptree):
        render_parse_tree(tree, render_ptree, same_rank, output_dot)

    print 'Done!'
