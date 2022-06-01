from lark import Lark, Transformer, v_args

grammar = """

    ?start: bexp

    ?bexp: bexp "||" bterm                               -> lor
        | bterm

    ?bterm: bterm "&&" notfactor                         -> land
        | notfactor

    ?notfactor: bfactor
        | "!" notfactor                                  -> lnot

    ?bfactor: bliteral 
        | bident 
        | nexp
        | relop

    ?nexp: term
        | nexp "+" term                                 -> add
        | nexp "-" term                                 -> sub

    ?term: factor
        | factor "*" term                               -> mul
        | factor "/" term                               -> div


    ?factor: NUMBER                                     -> number
        | "-" factor                                    -> neg
        | NAME                                          -> identifier
        | "(" nexp ")"
    
    ?relop: nexp ">" nexp                               -> greaterthan
        | nexp ">=" nexp                                -> greaterthanorequal
        | nexp "<"  nexp                                -> lessthan
        | nexp "<=" nexp                                -> lessthanorequal
        | nexp "==" nexp                                -> equalequal
        | nexp "!=" nexp                                -> notequal
        |  "(" relop ")"  

    ?bliteral: "F"                                      -> false
        | "T"                                           -> true
        | "(" bexp ")"
    
    ?bident: NAME ":=" bexp                             -> assign_idvar
            


%import common.CNAME -> NAME
%import common.NUMBER
%ignore " "
"""


@v_args(inline=True) 
class BooleanInterpreter(Transformer):
    number = float

    def __init__(self):
        self.vars = {}
        self.true()
        self.false()

    def assign_idvar(self, name, value):
        self.vars[name] = value
        return value

    def identifier(self, name):
        try:
            return self.var[name]
        except:
            return f"{name} variable not found"

    def add(self, e1, e2):
        neval =  int(e1) + int(e2)
        return neval

    def sub(self, e1, e2):
        neval =  int(e1) - int(e2)
        return neval
    
    def mul(self, e1, e2):
        neval =  int(e1) * int(e2)
        return neval
    
    def div(self, e1, e2):
        neval =  int(e1) / int(e2)
        return neval
    
    def neg(self, e1):
        neval =  int(e1)
        neval = -neval
        return neval


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

    def greaterthan(self, e1, e2):
        if e1 > e2:
            return True
        else:
            return False

    def greaterthanorequal(self, e1, e2):
        if e1 >= e2:
            return True
        else:
            return False
    
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

    def equalequal(self, e1, e2):
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
        eval = input('> ')
        if eval != 'Quit':
            print("answer>",calc(eval))
        else:
            print("Thankyou for using!")
            break
        
if __name__ == '__main__':
    main()