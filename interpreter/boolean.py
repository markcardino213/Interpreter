from lark import Lark, Transformer, v_args

grammar = """
    ?start: NUMBER "<" NUMBER                               -> lessthan
        | NUMBER "<=" NUMBER                                -> lessthanorequal
        | NUMBER ">"  NUMBER                                -> morethan
        | NUMBER ">=" NUMBER                                -> morethanorequal
        | NUMBER "==" NUMBER                                -> equalto
        | NUMBER "!=" NUMBER                                -> notequal
        |  "(" NUMBER ")"       

%import common.NUMBER
%ignore " "
"""



@v_args(inline=True) 
class BooleanInterpreter(Transformer):
    
    def lessthan(self, e1, e2):
        if e1 < e2:
            return True
        else:
            return False
    def lessthanorequal(self, e1, e2):
        if e1 <= e2:
            return True
        else:
            return False

    def morethan(self, e1, e2):
        if e1 > e2:
            return True
        else:
            return False
    
    def morethanorequal(self, e1, e2):
        if e1 >= e2:
            return True
        else:
            return False

    def equalto(self, e1, e2):
        if e1 == e2:
            return True
        else:
            return False

    def notequal(self, e1, e2):
        if e1 != e2:
            return True
        else:
            return False

parser = Lark(grammar)
tree = parser.parse
parser2 = Lark(grammar, parser='lalr', transformer=BooleanInterpreter())
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