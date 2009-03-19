"""
  # YAREE (Yet Another Regular Expression Engine) #
  
  - Regular expression parser
  
  Grammar:
  
      <er> ::= <er_choice>

      <er_choice> ::= <er_concat> ['+' <er_choice>]

      <er_concat> ::= <er_star> ['.' <er_concat>]

      <er_star> ::= <er_atom> ['*']

      <er_atom> ::= '#' | <re_char> | '(' <er> ')'

      <re_char> ::= 'a'..'z' | 'A'..'Z'


  Examples:
  
      a     // [] = { a }
      #     // [] = { lambda }    (lambda = the empty string)
      r1r2  // [] = [r1] \/ [r2]  (Union)
      r1*   // [] = [r1]*         (Klenee star)
      (r1)  // [] = [r1]
"""

__license__ = 'LGPL'
__author__ = 'Giuliano Vilela (giulianoxt@gmail.com)'


from string import whitespace
from itertools import ifilter


class Rule(object):
    def __init__(self, name, childs = None, rule = 0):
        self.name = name
        self.rule = rule
        self.childs = [] if childs is None else childs

    def __str__(self):
        return self.preOrder('')
  
    def preOrder(self, idt):
        ch = '\n'.join(c.preOrder(idt + '  ') for c in self.childs)

        return '%s%s<%d,%d> [\n%s\n%s]' % (idt, self.name, self.rule, len(self.childs), ch, idt)

    def __getitem__(self, i):
        return self.childs[i]


class Token(object):
    def __init__(self, name, lexem):
        self.name = name
        self.lexem = lexem
  
    def __str__(self):
        return '%s[\'%s\']' % (self.name, self.lexem)

    def preOrder(self, ident):
        return ident + str(self)


class Lex(object):
    def __init__(self, input):
        if (input is not None):
            self.set_input(input)
    
    def set_input(self, input):
        self.istream = ifilter(lambda x : not x in whitespace, iter(input))
        self.prepare_next()

    def get(self):
        if (self.nxt is None):
            return None
        else:
            c = self.nxt
            self.prepare_next()
            return c

    def next(self):
        return self.nxt

    def is_done(self):
        return (self.nxt is None)

    def prepare_next(self):
        try:
            self.nxt = self.istream.next()
        except StopIteration:
            self.nxt = None


class SyntaxError(Exception):
    pass


class RegExpParser(object):
    def __init__(self, input = None):
        self.set_input(input)
    
    def set_input(self, input):
        self.lex = Lex(input)
    
    def parse(self):
        tree = self.re()
        
        if (not self.lex.is_done()):
            raise SyntaxError('Excessive input (next char = %c)' % (self.lex.next(),))
        
        return tree
    
    def re(self):
        return self.re_choice() # Rule('re', [self.re_choice()])

    def re_choice(self):
        cnct = self.re_concat()
        
        if (self.lex.next() == '+'):
            tok = Token('choice_op', self.lex.get())
            chc = self.re_choice()
            return Rule('re_choice', [cnct, tok, chc], 1)
        
        return cnct # Rule('re_choice', [cnct])

    def re_concat(self):
        st = self.re_star()
        
        if (self.lex.next() == '.'):
            tok = Token('concat_op', self.lex.get())
            cnct = self.re_concat()
            return Rule('re_concat', [st, tok, cnct], 1)
        
        return st # Rule('re_concat', [st])

    def re_star(self):
        at = self.re_atom()
        
        if (self.lex.next() == '*'):
            tok = Token('star_op', self.lex.get())
            return Rule('re_star', [at, tok], 1)
    
        return at # Rule('re_star', [at])

    def re_atom(self):
        next = self.lex.next()
        
        if (next == '#'):
            tk = Token('lambda', self.lex.get())
            return tk # Rule('re_atom', [tk])
        elif (next == '('):
            ltk = Token('left_parenteses', self.lex.get())
            re = self.re()
            
            if (not self.lex.next() == ')'):
                raise SyntaxError('Expected \')\' at input')
            
            rtk = Token('right_parenteses', self.lex.get())

            return Rule('re_atom', [ltk, re, rtk], 2)
        else:
            return self.re_char() # Rule('re_atom', [self.re_char()], 1)
        
    def re_char(self):
        nx = self.lex.next()
        
        if ('a' <= nx <= 'z' or 'A' <= nx <= 'Z'):
            return Token('re_char', self.lex.get())
        else:
            s = 'but reached end of input' if nx is None else 'got a \'%c\' instead' % (nx)
            
            raise SyntaxError('Expected a character, ' + s)
