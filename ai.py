# PYTHON AI MODULE
# (C) Mauro Gaspari
# University of Bologna

"""Symbolic global constants, like. 'None', 'NOT_FOUND', etc."""

__all__ = [
    'Symbol','NOT_GIVEN','NOT_FOUND','AND','OR','NOT','IF','IFF','THEN','WHEN','FSymbol','Variable','FWRule','BWRule','unify','kb','rename_variables','rename_copy', 'defvar', 'defvarp', 'internal_types'
]

import string
import operator
import sys
import __builtin__

sys.setrecursionlimit(1000000000)

class Infix:

    """Infix operators for rules"""
    
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

class BSymbol(object):

    """Symbolic global constant"""

    __slots__ = ['_name', '_module']
    __name__   = property(lambda s: s._name)
    __module__ = property(lambda s: s._module)
    LogicalOperators = ["AND","OR","IF","IFF","NOT"]

    def __init__(self, symbol, moduleName=__name__):
        self.__class__._name.__set__(self,symbol)
        self.__class__._module.__set__(self,moduleName)

    def __reduce__(self):
        return self._name

    def __setattr__(self,attr,val):
        raise TypeError("Symbols are immutable")

    def __repr__(self):
        return self.__name__

    def __or__(self, other):
        return Cons(self,other)
    
#    __str__ = __repr__

class Cons():
    
    def __init__(self,car,cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return "["+str(self.car)+"|"+str(self.cdr)+ "]"

#    def __repr__(self):
#        return "["+str(self.car)+"|"+str(self.cdr)+ "]"


class Symbol():
    
    LogicalOperators = ["AND","OR","IF","IFF","NOT"]

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

    def __or__(self, other):
        return Cons(self,other)
    

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

# dereference
def deref(var,env):
    if isinstance(var, Variable) and var.name in env:
      return deref(env[var.name],env)
    elif isinstance(var,Cons):
        tail = deref(var.cdr,env)
        if type(tail) == type([]):
            return [deref(var.car,env)]+tail
        else:
            return [deref(var.car,env)]+[tail]
        return [deref(var.car,env)]+deref(var.cdr,env)  # ? maybe useless
    elif type(var) == type((1, )):
        return deref_tuple(var,env)
    elif type(var) == type([]):
        return deref_list(var,env)
    else:
        return var
    

def deref_list(list,env):
    newlist = []
    for x in list:
        if type(x) == type((1, )):
            newlist.append(deref_tuple(x,env))
        elif type(x) == type([]):
            newlist.append(deref_list(x,env))
#        elif isinstance(x,Variable) and x.name in env:
#            newlist.append(deref(env[x.name],env))
        else:
            newlist.append(deref(x,env))
    return newlist

def deref_tuple(tuple,env):
    newtuple = ()
    for x in tuple:
        if type(x) == type((1, )):
            newtuple += (deref_tuple(x,env),)
        elif type(x) == type([]):
            newtuple += (deref_list(x,env),)
        else:
            newtuple += (deref(x,env),)
    return newtuple

# rename variables

def get_variables(sequence):
    vlist = []
    for x in sequence:
        if type(x) == type((1, )) or type(x) == type([]):
            vlist += get_variables(x)
        elif isinstance(x,Variable):
            vlist.append(x)
    return vlist

# generate a new variable

def generate_variable(name,n):
    return Variable(name+str(n))

        
class FSymbol(Symbol):
    
    def __init__(self,name):
        if name[0] in string.uppercase:
            raise TypeError("FSymbols begins with lowercase letters")
        elif name in Symbol.LogicalOperators:
            raise TypeError("This is a logical operator")
        else:
            Symbol.__init__(self,name)

    def __cmp__(self,other):
        if self.name == other.name:
            return 0
        else:
            return 1

THEN = Infix(lambda x,y:KB.__kb__.make_fc_rule(x,y))
IF = Infix(lambda x,y:KB.__kb__.make_bc_rule(x,y))
THAT = Infix(lambda x,y:KB.__kb__.make_and_concept(x,y))

class LOperator(Symbol):
    pass


def unify(x, y, s):
    """Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs. [Fig. 9.1]
    >>> unify(x + y, y + C, {})
    {y: C, x: y}
    """
    if s == None:
        return None
    elif x == y:
        return s
    elif isinstance(x,Variable):
        return unify_var(x, y, s)
    elif isinstance(y,Variable):
        return unify_var(y, x, s)
#    elif isinstance(x, Expr) and isinstance(y, Expr):
#        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str) or not x or not y:
        if (x == y):
            return s
        else:
            return None
    elif operator.isSequenceType(x) and operator.isSequenceType(y) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    elif isinstance(x,Cons) and isinstance(y,Cons):
        return unify(x.cdr, y.cdr, unify(x.car, y.car, s))
    elif isinstance(x,Cons) and operator.isSequenceType(y) and len(y) == 1:
        return unify(x.cdr, [], unify(x.car, y[0], s))
    elif isinstance(x,Cons) and operator.isSequenceType(y):
        return unify(x.cdr, y[1:], unify(x.car, y[0], s))
    elif isinstance(y,Cons) and operator.isSequenceType(x) and len(x) == 1:
        return unify(y.cdr, [], unify(y.car, x[0], s))
    elif isinstance(y,Cons) and operator.isSequenceType(x):
        return unify(y.cdr, x[1:], unify(y.car, x[0], s))
    else:
        return None

def is_variable(x):
    "A variable is an Expr with no args and a uppercase symbol as the op."
    return isinstance(x, Variable)

def unify_var(var, x, s):
    if var.name in s:
        return unify(s[var.name], x, s)
#    elif occur_check(var, x):
#        return None
    else:
        return extend(s, var.name, x)

def occur_check(var, x):
    "Return true if var occurs anywhere in x."
    if var == x:
        return True
    elif isinstance(x, Expr):
        return var.op == x.op or occur_check(var, x.args)
    elif not isinstance(x, str) and issequence(x):
        for xi in x:
            if occur_check(var, xi): return True
    return False


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val; return copy.
    >>> extend({x: 1}, y, 2)
    {y: 2, x: 1}
    """
    s2 = s.copy()
    s2[var] = val
    return s2

# If we restrict wm elements to arity 2 this can 
# be improved for ask and forward rules

def make_key(tuple):
    return str(tuple[0])+str(len(tuple)-1)

class KB:
    """"A common Working Memory following the OCML style 
    it contains ground relations only. Relations are represented by 
    python tuples.
    A simple indexing mechanism is provided"""
    __kb__="empty"

    def __init__(self):
        self.wm = {}
        self.bcr = {}
        self.fwr = []
        self.fwrnodes = {}
        KB.__kb__ = self

    def tell(self, tuple):
        "Add the sentence to the KB"
        key = make_key(tuple)
        self.wm.setdefault(key,[]).append(tuple)

    def make_bc_rule(self,head, body):
        key = make_key(head)
        self.bcr.setdefault(key,[]).append((head,body))

    def make_fc_rule(self,head,body):
        self.fwr.append(FWRule(head,body))
        
    def ask(self, query, mores=True):
        """Ask returns a substitution that makes the query true, or
        it returns False. It is implemented in trems of ask_generator."""
        key = make_key(query)
        gvars = get_variables(query)
        iterator = self.wm[key].__iter__()
        try:
            r = unify(iterator.next(),query,{})
            while True:
                if r: 
                    for x in gvars:
                        print x.name+": "+str(deref(x,r))
                    # print r
                    if query_yes_no("more solutions?","no")== "no":
                        return True
                r =  unify(iterator.next(),query,{})
        except StopIteration:
            return False

    def ask_generator(self, query):
        "Yield all the substitutions that make query true."
        abstract

    def retract(self, sentence):
        "Remove the sentence from the KB"
        abstract

    # Prove backward rules, if wm is True it also checks
    # ground facts in the wm.
    def prove(self, goals, wm=False):
        gvars = get_variables(goals)
        bcprove(self,goals,{},wm,gvars,print_args_and_return_env)

# Schema for backward proof.
# bcprove(self,goals,env,wm,gvars,ret_fun)
# goals --> prolog query
# env
# wm --> bolean value, use or not use wm facts in the prove.
# gvars --> goal variables
# ret_fun --> function to return at the end (optional).


# Useful functions

def print_args_and_return_env(gvars,env):
    for x in gvars:
        print x.name+": "+str(deref(x,env))
    if query_yes_no("more solutions?","no") == "no":
        return env
    else:
        return False


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

class Role(FSymbol):
    
    def __init__(self,name,rdomain="",rrange="",dv=None,minc=None,maxc=None):
        self.domain = rdomain
        self.range = rrange
        self.default_value =dv
        self.min_cardinality=minc
        self.max_cardinality=maxc
        self.rule_list = []
        FSymbol.__init__(self,name)
        

class Predicate(FSymbol):

    pass

class Concept(FSymbol):
    
    def __init__(self,name,slots=[]):
        self.name = name
        self.slots = {}
        for x in slots:
            self.slots[x[0]] = x[1]

    def instances(self,L):
       for sym in L:
            sym = FSymbol(iname)
            KB.__kb__.tell((has_type,sym,self))
    
    def instance(self,iname,values=[]):
        defsym(iname)
        sym = getsym(iname)
        KB.__kb__.tell((has_type,sym,self))
        for slot in self.slots:
            slot_sym = getsym(slot)
            sdv = slot_sym.default_value
            if sdv != None and unbound_slot(slot_sym,values):
                set_slot(self,sym,slot_sym,sdv)
        for couple in values:
            set_slot(self,sym,couple[0],couple[1])

    def __repr__(self):
        return self.name

    def __or__(self, other):
        return Cons(self,other)

def set_slot(obj,sym,slot,value):
    ctype = obj.slots[slot.name]
    if ctype in internal_types:
        KB.__kb__.tell((slot,sym,value))
    else:
        defsym(value)
        myobj = getsym(value)
        KB.__kb__.tell((slot,sym,myobj))
        KB.__kb__.tell((has_type,myobj,ctype))


def unbound_slot(slot,values):
    print slot
    print type(slot)
    print values
    for couple in values:
        if slot == couple[0]:
            return False
    return True

def set_slot_type(slot,stype):
    if (type(bool)==type(stype)):
        return (slot,internal_type(stype))
    elif not checksym(stype):
       defsym(stype) 
       return (slot,getsym(stype))
    else:
        return (slot,getsym(stype))

def parse_slot_description(concept,role,tuple):
#    print tuple
    if tuple == ():
        return
    else: 
        if tuple[0] == has_type:
            rdomain = getsym(concept)
            role.domain = rdomain
            KB.__kb__.tell((has_domain,role,rdomain))
            if (type(bool)==type(tuple[1])):
                rrange = internal_type(tuple[1])
            else:
                rrange = getsym(tuple[1])
            role.range = rrange
            KB.__kb__.tell((has_range,role,rrange))
        elif tuple[0] == default_value:
            if role.range in internal_types:
                role.default_value = tuple[1]
            elif not checksym(tuple[1]):
                defsym(tuple[1])
                role.default_value = getsym(tuple[1])
            else:
                role.default_value = getsym(tuple[1])
        parse_slot_description(concept,role,tuple[2:])
    
def defconcept(name,slots=[]):
    slotnames = []
    for x in slots:
        slotnames.append(set_slot_type(x[0],x[2]))
    print slotnames
    command = "__builtin__."+name+"=Concept('"+name+"',"+str(slotnames)+")"
    exec command
    for x in slots:
        if not checksym(x[0]):
            defrole(x[0])
        else:
            print "warning symbol %s already defined" % x[0]
        parse_slot_description(name,getsym(x[0]),x[1:])

def internal_type(x):
    if x == bool:
        return bools
    elif x == str:
        return strs
    elif x == float:
        return floats
    elif x == int:
        return ints
    else:
        return x

def type_internal(x):
    if x == bools:
        return bool
    elif x == strs:
        return str
    elif x == floats:
        return float
    elif x == ints:
        return int
    else:
        return x
    
def defpredicate(sym):
    command = "__builtin__."+sym+"=Predicate('"+sym+"')"
    exec command

# Defining variables, functional symbols and logic operators
def defvar(var):
    command = "__builtin__."+var+"=Variable('"+var+"')"
    exec command

def defsym(sym):
    command = "__builtin__."+sym+"=FSymbol('"+sym+"')"
    exec command#

def defrole(sym):
    command = "__builtin__."+sym+"=Role('"+sym+"')"
    exec command

def deflop(lop):
    command = "__builtin__."+lop+"=LOperator('"+lop+"')"
    exec command

def getsym(str):
    return __builtin__.__dict__[str]

# checks if a given symbol is already definend

def checksym(str):
    return  __builtin__.__dict__.has_key(str)


NOT_GIVEN   = Symbol("NOT_GIVEN")
NOT_FOUND   = Symbol("NOT_FOUND")

#This function sets up common variable names
#and logic operators and returns a new KB
#possibly to be extended

def init():
    kb=KB()
    # initializing standard variables
    # variables are uppercase letters
    defvar('_')
    for var in string.uppercase:
        defvar(var)
        defvar(var+"1")
        defvar(var+"2")
        defvar(var+"3")
    # initializing built-in logic operators
    # this operators are reserved for the python AI module
    # a variant of the manchester OWL syntax is used for description logic
    defsym("is_a")
    defsym("builtin_type")
    defsym("default_value")
    defsym("has_type")
    defsym("has_range")
    defsym("has_domain")
    defsym("one_of")
    defsym("subclass_of")
    defsym("equivalent_to")
    defsym("disjoint_with")
    deflop("AND")
    deflop("OR")
    deflop("NOT")
    # standard operators of the OWL Manchester Syntax
    deflop("SOME")
    deflop("ONLY")
    deflop("MIN")
    deflop("MAX")
    deflop("EXACTLY")
    deflop("VALUE")
    deflop("IFF")
    deflop("ONLYSAME")
    return(kb)

# Infix builtin operators
__builtin__.IF= IF
__builtin__.THEN= THEN
__builtin__.THAT= THAT

# internal types symbols
defsym("bools")
defsym("strs")
defsym("ints")
defsym("floats")
internal_types = [ints, bools, strs, floats]

