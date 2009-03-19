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
    
    def first(self, state):
        self.first_s = state
        
    def final(self, state):
        self.final_s.add(state)
    
    def accepts(self, w, engine = 'nfa'):
        if (engine == 'nfa'):
            return self.run_nfa(w)
        elif (engine == 'dfa'):
            return self.run_dfa(w)
    
    def states(self):
        return self.fsa.iterkeys()
    
    def transitions(self):
        for s1, m in self.fsa.iteritems():
            for c, s_set in m.iteritems():
                for s2 in s_set:
                    yield (s1, s2, c)
    
    def __len__(self):
        return len(self.fsa)
    
    def run_dfa(self, w):
        s = self.first_s
        
        for c in w:
            s = iter(self.fsa[s][c]).next()
        
        return (s in self.final_s)
    
    def run_nfa(self, w):
        lc = self.lambda_closure()
        st_now = set((self.first_s,))
        
        for c in w:
            st_next = set()
            
            for st in st_now:
                for s in lc[st]:
                    st_next |= self.fsa[s][c] 
            
            st_now = st_next
            
            if (not st_now): return False
            
        return bool(st_now & self.final_s)
        
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

    def __iadd__(self, rhs):
        if (hasattr(rhs, '__iter__')):
            for s in rhs:
                self.add_state(s)
        else:
            self.add_state(rhs)
        
        return self

    def __setitem__(self, (s1, c), s2):
        self.add_transition(s1, s2, c)


if __name__ == '__main__':
    from re_graphviz import render_fsa    
    
    # Creates a FSA given its alphabet
    fsa = FSA('abc')
    
    # Adds 3 new states
    fsa += [0, 1, 2]
    
    # Adds five new transition edges (note that it's in fact non-deterministic)
    fsa[0,'#'] = 1
    fsa[0,'a'] = 0 # Transition from 0, consuming 'a', to 0 
    fsa[1,'b'] = 1
    fsa[1,'#'] = 2 # Transition from 1 to 2 consuming nothing (lambda transition)
    fsa[2,'c'] = 2
    
    # Sets the initial state
    fsa.first(0)
    
    # Sets a final state (can have more than one too)
    fsa.final(2)
    
    # Runs the acceptance engine of the FSA, returning True or False
    print fsa.accepts('aaaabbbbbccccc')
    
    # Renders the 
    render_fsa(fsa, 'fsa.png')
