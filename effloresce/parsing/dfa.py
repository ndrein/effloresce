"""Format for a DFA"""


import collections


Token = collections.namedtuple('Token', ['type', 'lexeme'])


class CantTokenize(Exception):
    pass


class DFA:
    @staticmethod
    def init_transitions(alphabet, states):
        """
        :return: transitions dict initialized to None
        """
        transitions = dict()
        for state in states:
            for symbol in alphabet:
                transitions[state, symbol] = None
        return transitions

    @staticmethod
    def build_multiple_transitions(transitions, beginning_state, symbols, end_state):
        """
        Modify the transitions dict to transition from beginning_state to end_state on all of the symbols
        :param transitions: transitions dict
        :return: modified transitions dict
        """
        for symbol in symbols:
            transitions[beginning_state, symbol] = end_state
        return transitions

    def __init__(self, alphabet, states, start_state, accept_states, transitions, state_map):
        """
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: set of states - can be represented by an int - cannot be None
        :param start_state: start state \in states
        :param accept_states: set of accepting states
        :param transitions: 2-dimensional dictionary
                            state x symbol -> state
        :param state_map: dict: state -> token type
                          (eg. if we end up in this state, what kind of token did we munch)
                          (eg. "var" state -> ID)
        """
        assert(start_state in states)
        assert(set(accept_states) < set(states))
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.state_map = state_map

    def transition(self, state, symbol):
        return self.transitions[state, symbol]

    def is_accepting(self, state):
        return state in self.accept_states

    def tokenize(self, input):
        """
        Take a sequence of input and return an array of Tokens

        :param input: iterable of symbols
        :return: iterable of Tokens
        :raises: CantTokenize
        """
        tokens = []

        while len(input) > 0:
            input, token = self.munch(input)
            tokens.append(token)

        return tokens

    def is_transition_possible(self, input, current_state):
        """
        Determine whether we can continue to munch input given that we are currently in current_state
        """
        return len(input) > 0 and self.transition(current_state, input[0]) != None

    def munch(self, input):
        """
        Read in symbols from the input and either return a Token or throw an error
        Uses simplified Maximal Munch

        :param input: iterable of symbols
        :return: modified input, Token
        :raises: CantTokenize
        """
        current_state = self.start_state
        lexeme = ""

        while self.is_transition_possible(input, current_state):
            current_state = self.transition(current_state, input[0])
            lexeme += input[0]
            input = input[1:]

        if self.is_accepting(current_state): # Emit viable token
            return input, Token(self.state_map[current_state], lexeme)
        else:
            # TODO: backtrack for Maximal Munch
            raise CantTokenize()

