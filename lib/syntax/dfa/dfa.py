"""
Format for a DFA
"""

import collections
import string

# TODO: can't have tokenization here
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


    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        """
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: cannot be None (the representation of the error state)
        :param start_state: one of the given states
        :param accept_states: set of accepting states
        :param transitions: dict: (state x symbol) -> state
                                  If a mapping is undefined, the mapping defaults to the error state
        """
        assert(start_state in states)
        assert(set(accept_states) < set(states))

        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def transition(self, state, symbol):
        """
        :return: a valid state if possible, otherwise the error state
        """
        return self.transitions[state, symbol] if (state, symbol) in self.transitions else ERROR_STATE

    def is_accepting(self, state):
        return state in self.accept_states

    def can_traverse_more(self, current_state, input):
        """
        Determine whether we can continue to process the input
        """
        return len(input) > 0 and self.transition(current_state, input[0]) != ERROR_STATE

    def traverse(self, input):
        """
        Partition the input into consumed and remaining input, and return the final state
        Uses simplified Maximal Munch

        :param input: iterable of symbols
        :return: list of munched symbols, list of remaining input, final valid state
        :raises: CantTokenize
        """
        current_state = self.start_state
        consumed, remaining = input[0:0], input
        # TODO: should our interface be strictly in lists?

        while self.can_traverse_more(current_state, remaining):
            current_state = self.transition(current_state, remaining[0])
            # TODO find more efficient solution like append
            consumed, remaining = consumed + remaining[0], remaining[1:]

        if self.is_accepting(current_state):
            return consumed, remaining, current_state
        else:
            # TODO: backtrack for Maximal Munch
            raise CantTokenize()

