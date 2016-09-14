"""Create the DFA specific to logical formulas"""
#TODO: add support for <, >, <=, >=, =, +, -, *, /, %, _

import string

from lib.syntax.scanner import Scanner


letters = set(string.ascii_letters)
numbers = set(string.digits)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ALPHABET
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

alphabet = letters | numbers | set('()&|!-<>,')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
STATES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

states = {'start',
          'bool',
          'f', 'fo', 'for', 'fora', 'foral', 'forall',
          'e', 'ex', 'exi', 'exis', 'exist', 'exists',
          'id',
          'num',
          '!',
          '&', '&&',
          '|', '||',
          '-', '->',
          '<', '<-', '<->',
          '(',
          ')',
          ','}


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
START STATE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

start_state = 'start'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ACCEPT STATES
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
accept_states = {'id',
                 'bool',
                 'f', 'fo', 'for', 'fora', 'foral', 'forall',
                 'e', 'ex', 'exi', 'exis', 'exist', 'exists',
                 'num',
                 '!', '&&', '||', '->', '<->',
                 '(', ')', ','}


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
TRANSITIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

transitions = dict()

####################################################################################################
# BOOL

transitions['start', 'T'] = 'bool'
transitions['start', 'F'] = 'bool'
transitions = Scanner.DFA.build_multiple_transitions(transitions, 'bool', letters, 'id')

####################################################################################################
# ID

transitions = Scanner.DFA.build_multiple_transitions(transitions, 'start', letters - {'f', 'e', 'T', 'F'}, 'id')
transitions = Scanner.DFA.build_multiple_transitions(transitions, 'id', letters, 'id')

####################################################################################################
# FORALL

transitions['start', 'f'] = 'f'
# Beginning with state 'f', if we see an 'o', go to state 'fo', otherwise go to 'id' on any other letter
transitions = Scanner.DFA.build_complement_transitions(transitions, 'f', letters, 'o', 'fo', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'fo', letters, 'r', 'for', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'for', letters, 'a', 'fora', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'fora', letters, 'l', 'foral', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'foral', letters, 'l', 'forall', 'id')
transitions = Scanner.DFA.build_multiple_transitions(transitions, 'forall', letters, 'id')

####################################################################################################
# EXISTS

transitions['start', 'e'] = 'e'
transitions = Scanner.DFA.build_complement_transitions(transitions, 'e', letters, 'x', 'ex', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'ex', letters, 'i', 'exi', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'exi', letters, 's', 'exis', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'exis', letters, 't', 'exist', 'id')
transitions = Scanner.DFA.build_complement_transitions(transitions, 'exist', letters, 's', 'exists', 'id')
transitions = Scanner.DFA.build_multiple_transitions(transitions, 'exists', letters, 'id')

####################################################################################################
# NUMBERS

transitions = Scanner.DFA.build_multiple_transitions(transitions, 'start', numbers, 'num')
transitions = Scanner.DFA.build_multiple_transitions(transitions, 'num', numbers, 'num')

####################################################################################################
# LOGICAL OPERATORS

transitions['start', '!'] = '!'
transitions['start', '&'] = '&'
transitions['&',     '&'] = '&&'
transitions['start', '|'] = '|'
transitions['|',     '|'] = '||'
transitions['start', '-'] = '-'
transitions['-',     '>'] = '->'
transitions['start', '<'] = '<'
transitions['<',     '-'] = '<-'
transitions['<-',    '>'] = '<->'
transitions['start', '('] = '('
transitions['start', ')'] = ')'
transitions['start', ','] = ','


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
STATE MAP
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Map each state to a token type
# eg. 'fo' -> 'ID'

state_map = dict()

state_map['bool'] = 'BOOL'

for state in {'f', 'fo', 'for', 'fora', 'foral',
              'e', 'ex', 'exi', 'exis', 'exist',
              'id'}:
    state_map[state] = 'ID'

state_map['forall'] = 'FORALL'
state_map['exists'] = 'EXISTS'

state_map['num'] = 'NUM'

state_map['!'] = 'NOT'
state_map['&&'] = 'AND'
state_map['||'] = 'OR'
state_map['->'] = 'IMPLIES'
state_map['<->'] = 'IFF'

state_map['('] = 'LPAREN'
state_map[')'] = 'RPAREN'
state_map[','] = 'COMMA'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGIC DFA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# You're supposed to import this
logic_scanner = Scanner(Scanner.DFA(alphabet, states, start_state, accept_states, transitions, state_map, token_delimiters=string.whitespace))
