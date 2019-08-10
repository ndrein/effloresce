"""
Grammar for formulas in propositional logic
"""

GRAMMAR = """
?start: LITERAL
         | "(NOT" start ")" -> not
         | "(" start "OR" start ")" -> or
         | "(" start "AND" start ")" -> and
         | "(" start "IMPLIES" start ")" -> implies
         | "(" start "IFF" start ")" -> iff
         | "(" start "NAND" start ")" -> nand
LITERAL: /[a-z]+/

%import common.WS
%ignore WS
"""
