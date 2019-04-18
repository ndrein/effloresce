LOGIC_GRAMMAR = '''
?start: LITERAL
         | "(NOT" start ")" -> not
         | "(" start "OR" start ")" -> or
         | "(" start "AND" start ")" -> and
         | "(" start "IMPLIES" start ")" -> implies
         | "(" start "IFF" start ")" -> iff
LITERAL: /[a-z]+/

%import common.WS
%ignore WS
'''
