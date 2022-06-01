from lark import Lark, Transformer, v_args

grammar = """
    ?start: lexp

    ?lexp: lexp "|" conj            -> lor
        | conj             

    ?conj: conj "&"lval             -> land
        |  lval

    ?lval: val
        | "!" lval                  -> lnot

    ?val: "T"                       -> true
        | "F"                       -> false
        | "(" lexp ")"
    

%import common.WS
%ignore " "
"""


@v_args(inline=True) 
class LogicExp(Transformer):
    
    def __init__(self):
        self.true()
        self.false()

    def true(self):
        true = True
        return true
    
    def false(self):
        false = False
        return false

    def lor(self, true, false):
        if true or false:
            return self.true()
        else:
            return  self.false()
    
    def land(self, true, false):
        if true and false:
            return self.true()
        else:
            return  self.false()

    def lnot(self, n):
        if not n == self.true():
            return True
        elif not n == self.false():
            return False
        else:
            return f"Invalid Expression"



parser = Lark(grammar)
tree = parser.parse
parser2 = Lark(grammar, parser='lalr', transformer=LogicExp())
calc = parser2.parse

def main():
    while True:
        eval = input('> ')
        if eval != 'Quit':
            print(tree(eval).pretty())
            print("answer>",calc(eval))
        else:
            print("Thankyou for using!")
            break

if __name__ == '__main__':

    main()