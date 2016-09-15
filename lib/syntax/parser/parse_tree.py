# TODO: make polymorphism for each type of node?


class ParseTree:
    def type(self):
        return self.type


class NonTerminalNode(ParseTree):
    def __init__(self, type, children):
        self.type = type
        self.children = children

    # TODO: use foldr to assemble string
    def lhs(self):
        lhs = ''
        for child in self.children:
            lhs += child.type()
        return lhs

    def __repr__(self):
        # TODO: use foldr to assemble string of children
        return self.type + ' ->'


class TerminalNode(ParseTree):
    """Leaves of the ParseTree"""
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __repr__(self):
        return self.type + ' ' + self.lexeme
