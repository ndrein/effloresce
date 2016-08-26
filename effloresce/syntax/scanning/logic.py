"""Create the DFA specific to logical formulas"""
#TODO: add support for <, >, <=, >=, =, +, -, *, /, %, _

import string

from .dfa import DFA


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
accept_states = {'id', 'forall', 'exists', 'num', '!', '&&', '||', '->', '<->', '(', ')', ','}


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
TRANSITIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

transitions = DFA.init_transitions(alphabet, states)

####################################################################################################
# ID

transitions = DFA.build_multiple_transitions(transitions, 'start', letters - {'f', 'e'}, 'id')
transitions = DFA.build_multiple_transitions(transitions, 'id', letters, 'id')

####################################################################################################
# FORALL

transitions['start', 'f'] = 'f'
# Beginning with state 'f', if we see an 'o', go to state 'fo', otherwise go to 'id' on any other letter
transitions = DFA.build_complement_transitions(transitions, 'f', letters, 'o', 'fo', 'id')
transitions = DFA.build_complement_transitions(transitions, 'fo', letters, 'r', 'for', 'id')
transitions = DFA.build_complement_transitions(transitions, 'for', letters, 'a', 'fora', 'id')
transitions = DFA.build_complement_transitions(transitions, 'fora', letters, 'l', 'foral', 'id')
transitions = DFA.build_complement_transitions(transitions, 'foral', letters, 'l', 'forall', 'id')
transitions = DFA.build_multiple_transitions(transitions, 'forall', letters, 'id')

####################################################################################################
# EXISTS

transitions['start', 'e'] = 'e'
transitions = DFA.build_complement_transitions(transitions, 'e', letters, 'x', 'ex', 'id')
transitions = DFA.build_complement_transitions(transitions, 'ex', letters, 'i', 'exi', 'id')
transitions = DFA.build_complement_transitions(transitions, 'exi', letters, 's', 'exis', 'id')
transitions = DFA.build_complement_transitions(transitions, 'exis', letters, 't', 'exist', 'id')
transitions = DFA.build_complement_transitions(transitions, 'exist', letters, 's', 'exists', 'id')
transitions = DFA.build_multiple_transitions(transitions, 'exists', letters, 'id')

####################################################################################################
# NUMBERS

transitions = DFA.build_multiple_transitions(transitions, 'start', numbers, 'num')
transitions = DFA.build_multiple_transitions(transitions, 'num', numbers, 'num')

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
logic_dfa = DFA(alphabet, states, start_state, accept_states, transitions, state_map, token_delimiters=string.whitespace)
