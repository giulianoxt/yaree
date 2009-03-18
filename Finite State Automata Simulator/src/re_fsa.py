"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - Finite State Automata implementation
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


from collections import defaultdict


class FSA(object):
    def __init__(self, alph = None):
        self.alph = alph
        self.fsa = { } # { node -> { c -> set(node) } }
        
        self.first_s = None
        self.final_s = set()
    
    def add_state(self, state):
        self.fsa[state] = defaultdict(lambda : set())

    def add_transition(self, s1, s2, c):
        self.fsa[s1][c].add(s2)
    
    def set_first(self, state):
        self.first_s = state
        
    def set_final(self, state):
        self.final_s.add(state)
        
    def run_dfa(self, w):
        s = self.first_s
        
        for c in w:
            s = iter(self.fsa[s][c]).next()
        
        return (s in self.final_s)
    
    def run_nfa(self, w):
        st_now = set((self.first_s,))
        lc = self.lambda_closure()
        
        for c in w:
            for st in frozenset(st_now):
                st_now.update(lc[st]) 
        
            st_next = set()
            for s in st_now:
                st_next.update(self.fsa[s][c])
            
            st_now = st_next
            
            if (not len(st_now)): return False
            
        return len(st_now & self.final_s) > 0
        
    def lambda_closure(self):
        def visit(s, vis):
            if (s in vis): return

            vis.add(s)
                
            for st in self.fsa[s]['#']:
                visit(st, vis)
        
        lc = { } # { node -> set(node) }
        
        for s in self.fsa:
            lc[s] = set()
            visit(s, lc[s])
            
        return lc    


if __name__ == '__main__':
    fsa = FSA('abc')
    
    fsa.add_state('q0')
    fsa.add_state('q1')
    fsa.add_state('q2')
    
    fsa.add_transition('q0', 'q0', '0')
    fsa.add_transition('q0', 'q1', '#')
    fsa.add_transition('q1', 'q1', '1')
    fsa.add_transition('q1', 'q2', '#')
    fsa.add_transition('q2', 'q2', '2')
    
    fsa.set_first('q0')
    fsa.set_final('q2')
    
    print fsa.run_nfa('0011112222')
