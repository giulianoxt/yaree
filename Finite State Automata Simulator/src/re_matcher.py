"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - Regular Expression matcher
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


from re_fsa import FSA
from re_graphviz import render_fsa
from re_parser import RegExpParser, Token


class RegularExpression(FSA):
    def __init__(self, f):
        self.fsa = f.fsa
        self.first_s = f.first_s
        self.final_s = f.final_s
        self.lc = f.lc
    
    @staticmethod
    def compile(re):
        tree = RegExpParser(re).parse()
        
        fsa = fsa_from_tree(tree)
        fsa.simplify()
        fsa.compile()
        
        return RegularExpression(fsa)
    
    def match(self, str):
        return self.accepts(str, engine = 'nfa')

    def render_automata(self, filename):
        render_fsa(self, filename)


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


if __name__ == '__main__':
    from os import system
    
    re = RegularExpression.compile('(c.a + b* + d*.c) + a.a*')
    
    for s in ('aaa', 'bbbbbab', 'ddddc', 'aabda', 'bbbbbbcaaaaa'):
        print 'S =', s, '- Yes!' if re.match(s) else '- No.'
    
    re.render_automata('fsa.png')
    
    system('display fsa.png')
