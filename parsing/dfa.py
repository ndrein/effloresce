"""Format for a DFA"""


from collections import namedtuple


State = namedtuple('State', ['id', 'token_type'])
Token = namedtuple('Token', ['type', 'lexeme'])


class CantTokenize(Exception):
    pass


class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transitions):
        """
        Create a DFA
        States and alphabet are arbitrary, but must have the equality (=) operator defined on them

        :param alphabet: alphabet as a set
        :param states: set of states
        :param start_state: start state \in states
        :param accept_states: set of accepting states
        :param transitions: 2-dimensional dictionary
                            state x symbol -> state
        """
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def transition(self, state, symbol):
        return self.transitions[state][symbol]

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
        current_state = self.start_state

        for index, symbol in enumerate(input):
            if self.is_accepting(current_state):
                return input[index:], Token(current_state.token_type, input[:index])
            else:
                # Transition on symbol
                current_state = self.transition(current_state, symbol)

                # We have transitioned to the error state (None)
                if current_state == None:
                    raise CantTokenize()

        # If we have failed to return a token by the time we get to the end of the input, we must throw an error
        raise CantTokenize()
