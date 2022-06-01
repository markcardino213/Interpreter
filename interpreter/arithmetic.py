from lark import Lark, Transformer, v_args
import operator

grammar = """
    ?start: exp
        | NAME ":=" exp    -> assign_ident

    ?exp: term
        | exp "+" term   -> add
        | exp "-" term   -> sub

    ?term: factor
        | factor "*" term  -> mul
        | factor "/" term  -> div
        | factor "^" term  -> pow

    ?factor: NUMBER        -> number
        | "-" factor       -> neg
        | NAME             -> identifier
        | "(" exp ")"       

%import common.CNAME -> NAME
%import common.NUMBER
%ignore " "
"""


@v_args(inline=True) 
class CalculateTree(Transformer):
    number = float

    def __init__(self):
        self.var = {}

    def assign_ident(self, name, value):
        self.var[name] = value
        return value

    def identifier(self, name):
        try:
            return self.var[name]
        except:
            return f"{name} variable not found"
            
    def add(self, n1,n2):
        return operator.add(n1,n2)

    def sub(self, n1,n2):
        return operator.sub(n1,n2)
    
    def mul(self, n1,n2):
        return operator.mul(n1,n2)
    
    def div(self, n1,n2):
        return operator.truediv(n1,n2)
    
    def pow(self, n1,n2):
        return operator.pow(n1,n2)

parser = Lark(grammar)
tree = parser.parse
parser2 = Lark(grammar, parser='lalr', transformer=CalculateTree())
calc = parser2.parse


def main():
    while True:
        solve = input('input> ')
        if solve != 'Quit':
            print(tree(solve).pretty())
            print(calc(solve))
        else:
            print("Thankyou for using!")
            break

if __name__ == '__main__':

    main()