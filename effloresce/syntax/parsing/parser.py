class ProductionRule:
    def __init__(self, lhs, rhs):
        """
        :param lhs: Token type
        :param rhs: sequence of Token types
        """
        self.lhs = lhs
        self.rhs = rhs


class Parser:
    # TODO: decide whether to use LL(1), LR(1), etc.  Take a parsing dfa as parameter
    def __init__(self, production_rules):
        """
        :param production_rules: set of ProductionRules
        """
        self.production_rules = production_rules

    def parse(self, tokens):
        """
        :param tokens: sequence of Token.{type, lexeme}
        :return: ParseTree
        """
        # TODO
