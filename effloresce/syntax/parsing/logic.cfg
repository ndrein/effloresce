# TODO: CFG for logical formulas
formula -> ID LPAREN arglist RPAREN
formula -> BOOL
formula -> LPAREN formula AND formula RPAREN
formula -> LPAREN formula OR formula RPAREN
formula -> LPAREN formula IMPLIES formula RPAREN
formula -> LPAREN formula IFF formula RPAREN
formula -> LPAREN NOT formula RPAREN
formula -> LPAREN FORALL ID formula RPAREN
formula -> LPAREN EXISTS ID formula RPAREN
arglist -> expr
arglist -> expr COMMA arglist
expr -> ID
expr -> ID LPAREN RPAREN
expr -> ID LPAREN arglist RPAREN
