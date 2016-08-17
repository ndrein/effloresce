"""Format for a DFA"""


import collections


Token = collections.namedtuple('Token', ['type', 'lexeme'])


class CantTokenize(Exception):
    pass


class DFA:
    @staticmethod
    def init_transitions(alphabet, states):
        """
        :param alphabet:
        :param states:
        :return: transitions dict initialized to None
        """
        transitions = dict()
        for state in states:
            for symbol in alphabet:
                transitions[state, symbol] = None
        return transitions

    def __init__(self, alphabet, states, start_state, accept_states, transitions, state_map):
        """
        Create a DFA
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: set of states - can be represented by an int - cannot be None
        :param start_state: start state \in states
        :param accept_states: set of accepting states
        :param transitions: 2-dimensional dictionary
                            state x symbol -> state
        :param state_map: dict: state -> token type
                          (eg. if we end up in this state, what kind of token did we munch)
        """
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

    def munch(self, input):
        """
        Read in symbols from the input and either return a Token or throw an error
        Uses simplified Maximal Munch

        :param input: iterable of symbols
        :return: modified input, Token
        :raises: CantTokenize
        """
        prev_state = None
        current_state = self.start_state

        index = 0
        for index, symbol in enumerate(input):
            prev_state = current_state
            current_state = self.transition(current_state, symbol)

            # We can't munch anymore to build this token
            if current_state == None:
                break

        if self.is_accepting(current_state): # Emit viable token
            return input[index + 1:], Token(self.state_map[prev_state], input[:index + 1])
        else:
            # TODO: backtrack for Maximal Munch
            raise CantTokenize()

