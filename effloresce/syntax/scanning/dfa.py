"""Format for a DFA"""

import collections
import string


Token = collections.namedtuple('Token', ['type', 'lexeme'])


class CantTokenize(Exception):
    pass


# The error state is represented by None
ERROR_STATE = None


class DFA:
    @staticmethod
    def build_multiple_transitions(transitions, beginning_state, symbols, end_state):
        """
        Convenience method to add to the transitions dict to make a DFA
        Transition from beginning_state to end_state on all of the symbols
        :param transitions: transitions dict
        :param symbols: iterable of symbols
        :return: modified transitions dict
        """
        for symbol in symbols:
            transitions[beginning_state, symbol] = end_state
        return transitions

    @classmethod
    def build_complement_transitions(cls, transitions, beginning_state, symbols, a, end_state_a, end_state_b):
        """
        Convenience method to add to the transitions dict to make a DFA
        If we see an a, go to end_state_a
        If we see one of the given symbols that's not a, go to end_state_b

        :param transitions: transitions dict
        :param symbols: set of symbols
        :param a: symbol
        :return: modified transitions dict
        """
        transitions = cls.build_multiple_transitions(transitions, beginning_state, {a}, end_state_a)
        transitions = cls.build_multiple_transitions(transitions, beginning_state, symbols - {a}, end_state_b)
        return transitions


    def __init__(self, alphabet, states, start_state, accept_states, transitions, state_map, token_delimiters=string.whitespace):
        """
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: set of values with = operator defined - cannot be None (the representation of the error state)
        :param start_state: start state \in states
        :param accept_states: set of accepting states
        :param transitions: dict: (state x symbol) -> state
        :param state_map: dict: state -> token type
                          (eg. if we end up in this state, what kind of token did we munch)
                          (eg. "var" state -> ID)
        :param token_delimiters: set of symbols that separate tokens
                                 defaults to whitespace
        """
        assert(start_state in states)
        assert(set(accept_states) < set(states))

        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        self.state_map = state_map
        self.token_delimiters = token_delimiters

    def transition(self, state, symbol):
        """
        :return: a valid state if possible, otherwise the error state
        """
        return self.transitions[state, symbol] if (state, symbol) in self.transitions else ERROR_STATE

    def is_accepting(self, state):
        return state in self.accept_states

    def strip_leading_delimiters(self, input):
        """
        Remove all leading instances of self.token_delimiters

        :param input: iterable of input
        :return: modified input
        """
        return input.lstrip(self.token_delimiters)

    def can_munch_more(self, input, current_state):
        """
        Determine whether we can continue to munch input given that we are currently in current_state
        """
        return len(input) > 0 and input[0] not in self.token_delimiters and self.transition(current_state, input[0]) != ERROR_STATE

    def munch(self, input):
        """
        Read in symbols from the input and either return a Token or throw an error
        Uses simplified Maximal Munch

        :param input: iterable of symbols
        :return: modified input, Token
        :raises: CantTokenize
        """
        current_state = self.start_state
        lexeme = ''

        while self.can_munch_more(input, current_state):
            current_state = self.transition(current_state, input[0])
            lexeme += input[0]
            input = input[1:]

        if self.is_accepting(current_state): # Emit viable token
            return input, Token(self.state_map[current_state], lexeme)
        else:
            # TODO: backtrack for Maximal Munch
            raise CantTokenize()

