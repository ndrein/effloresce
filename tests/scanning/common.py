def compare_token_sequences(computed_tokens, correct_tokens):
    """
    Compare 2 sequences of tokens and raise an Exception if they are not equal
    """
    assert(len(computed_tokens) == len(correct_tokens))
    for correct_token, computed_token in zip(correct_tokens, computed_tokens):
        assert(correct_token.type == computed_token.type)
        assert(correct_token.lexeme == computed_token.lexeme)
