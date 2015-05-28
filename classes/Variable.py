import string

from Symbol import Symbol

class Variable(Symbol):
    
    def __init__(self,name): 
        #def __init__(self,name,module=__name__): Con Moduli

        if name[0] in string.lowercase:
            raise TypeError("Variables begins with Uppercase letters")
        elif name in Symbol.LogicalOperators:
            raise TypeError("This is a logical operator")
        else:
            Symbol.__init__(self,name)
            self.sname = name
            # Symbol.__init__(self,name,module)
            # self.id = Symbol(name)

    def __eq__(self,Var):
        return (isinstance(Var,Variable) and self.name == Var.name)

    def deref(self,env):
        if env.has_key(self.name):
            return deref(env[self.name],env)
        else:
            return self.name
    
    def __str__(self):
        return self.name

    def rename(self,n):
        self.name = "_"+self.sname+str(n)
