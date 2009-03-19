"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - Regular Expression matcher
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


from re_fsa import FSA
from re_parser import RegExpParser, Token


def fsa_from_tree(t):
    if isinstance(t, Token):
        return FSA([0,1], [(0,1,t.lexem)], 0, 1)
    
    if (t.name == 're_choice'):
        f1 = fsa_from_tree(t[0])
        f2 = fsa_from_tree(t[2])
        
        f1.alter_states(lambda x : x + 1)
        f2.alter_states(lambda x : x + 1 + len(f1))
        
        f = f1 + f2
        
        st = f.first(0)
        end = f.final(len(f1) + 1 + len(f2))
               
        f[st,'#'] = 1
        f[st,'#'] = 1 + len(f1)
        f[len(f1),'#'] = end
        f[end - 1,'#'] = end
        
        return f 
    
    elif (t.name == 're_star'):
        f1 = fsa_from_tree(t[0])
        
        f1.alter_states(lambda x : x + 1)
        
        st = f1.first(0)
        f1.final_s.clear()
        end = f1.final(len(f1))
        
        f1[st,'#'] = 1
        f1[end,'#'] = 0
        f1[st,'#'] = end
        f1[end-1,'#'] = end
        
        return f1
    
    elif (t.name == 're_atom'):
        return fsa_from_tree(t[1])
    
    elif (t.name == 're_concat'):
        f1 = fsa_from_tree(t[0])
        f2 = fsa_from_tree(t[2])
        
        f1.alter_states(lambda x : x + 1)
        f2.alter_states(lambda x : x + 1 + len(f1))
                
        f = f1 + f2
        
        st = f.first(0)
        end = f.final(len(f1) + 1 + len(f2))
               
        f[st,'#'] = 1
        f[len(f1),'#'] = len(f1) + 1
        f[end - 1,'#'] = end
        
        return f
    

def fsa_from_re(re):
    tree = RegExpParser(re).parse()
    
    return fsa_from_tree(tree)


if __name__ == '__main__':
    from os import system
    from re_graphviz import render_fsa
    
    fsa = fsa_from_re('((a.a + b.b + d)*.b.a.(c.c.c.d*))*')
    
    print fsa.accepts('aaaaaabbbbbbbacccdddddddddd')
    
    render_fsa(fsa, 'fsa.png')
    
    system('display fsa.png')
