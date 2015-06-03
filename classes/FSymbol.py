import string

from Symbol import Symbol

class FSymbol(Symbol):
    
    def __init__(self,name):
        if name[0] in string.uppercase:
            raise TypeError("FSymbols begins with lowercase letters")
        elif name in Symbol.LogicalOperators:
            raise TypeError("This is a logical operator")
        else:
            Symbol.__init__(self,name)

    def __cmp__(self,other):
        #if type(self) == type((1, )) or type(other) == type((1, )):
        #    return 1
        #el
        if self.name == other.name:
            return 0
        else:
            return 1
