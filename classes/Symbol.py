from Cons import Cons

class Symbol():
    
    LogicalOperators = ["AND","OR","IF","IFF","NOT"]

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

    def __or__(self, other):
        return Cons(self,other)
