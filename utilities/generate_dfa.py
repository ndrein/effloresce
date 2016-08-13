from string import ascii_lowercase, ascii_uppercase

def build_transitions(start_state, symbols, end_state):
    max_length = max(map(lambda(e): len(e), states))

    lst = []
    for symbol in symbols:
        lst.append(str(start_state) + ' ' * (max_length - len(start_state) + 1) + str(symbol) + ' ' * (max_length - len(end_state) +  1) + str(end_state))
    return lst


def write_dfa(filename, alphabet, states, initial_states, finish_states, transitions):
    with open(filename, 'w') as f:
        f.write(str(len(alphabet)) + '\n')
        for char in alphabet:
            f.write(str(char) + '\n')

        f.write(str(len(states)) + '\n')
        for state in states:
            f.write(str(state) + '\n')

        f.write(str(initial_state) + '\n')

        f.write(str(len(finish_states)) + '\n')
        for finish_state in finish_states:
            f.write(str(finish_state) + '\n')

        f.write(str(len(transitions)) + '\n')
        for transition in transitions:
            f.write(str(transition) + '\n')


############################################################################
##  DFA
############################################################################

filename = 'wlp4.dfa'

alphabet = list(ascii_lowercase) + list(ascii_uppercase) + range(0, 9 + 1) + list('(){}=!<>+-*/%,;[]&')
states = [
          'start',
          'singleSymbol',
          'equal',
          'doubleEqual',
          'lessThan',
          'lessThanOrEqual',
          'greaterThan',
          'greaterThanOrEqual',
          'not',
          'notEqual',
          'zero',
          'nonzeroNumeric',
          'alphanumeric'
          ]
initial_state = "start"
finish_states = ['singleSymbol', 'equal', 'doubleEqual', 'lessThan', 'lessThanOrEqual',
                 'greaterThan', 'greaterThanOrEqual', 'notEqual', 'zero', 'nonzeroNumeric', 'alphanumeric']


transitions = []
transitions += build_transitions('start', list('(){}+-*/%[]&;,'), 'singleSymbol')

transitions += build_transitions('start', ['='], 'equal')
transitions += build_transitions('equal', ['='], 'doubleEqual')

transitions += build_transitions('start', ['<'], 'lessThan')
transitions += build_transitions('lessThan', ['='], 'lessThanOrEqual')

transitions += build_transitions('start', ['>'], 'greaterThan')
transitions += build_transitions('greaterThan', ['='], 'greaterThanOrEqual')

transitions += build_transitions('start', ['!'], 'not')
transitions += build_transitions('not', ['='], 'notEqual')

transitions += build_transitions('start', ['0'], 'zero')

transitions += build_transitions('start', range(1, 9 + 1), 'nonzeroNumeric')
transitions += build_transitions('nonzeroNumeric', range(0, 9 + 1), 'nonzeroNumeric')

transitions += build_transitions('start', list(ascii_lowercase) + list(ascii_uppercase), 'alphanumeric')
transitions += build_transitions('alphanumeric', list(ascii_lowercase) + list(ascii_uppercase) + range(0, 9 + 1), 'alphanumeric')



if __name__ == "__main__":
    write_dfa(filename, alphabet, states, initial_state, finish_states, transitions)
