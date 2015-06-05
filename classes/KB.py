import copy
from sys import stdin

from Variable import Variable
from Printer import Printer
from FSymbol import FSymbol
from Unify import Unify
from Cons import Cons

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

    def make_key(self,tuple):
        return str(tuple[0])+str(len(tuple)-1)

    def printRule(self, element):
        if element == None:
            return str(None)
        elif isinstance(element, str) or isinstance(element, int) or isinstance(element, bool):
            return str(element)
        elif isinstance(element, Variable):# or isinstance(element, instance):
            return element.__str__()
        elif (isinstance(element,Cons)):
            return " | ".join( [ self.printRule(element.car), self.printRule(element.cdr) ])

        list = []
        
        if type(element) == type([]):
            for i in element:
                list.append(self.printRule(i))
            return "[" + ", ".join(list) + "]"

        if type(element) == type({}):
            for i in element:
                list.append( self.printRule(i) + " : " + self.printRule(element[i]) )
            return "{" + ", ".join(list) + "}"

        #print type(element)
        for i in element:
            if (isinstance(i,Cons)):
                list.append( " | ".join( [ self.printRule(i.car), self.printRule(i.cdr) ]))
            elif type(i) == type((1, )):
                list.append(str(self.printRule(i)))
            else:
                #print type(i)
                list.append(str(i))

        return "(" + ", ".join(list) + ")"

    def printRules(self):
        for key in self.bcr:
            for element in self.bcr[key]:
                print self.printRule(element[0]) + " :- " + self.printRule(element[1]) + "."
        
        print ""

    def get_variables(self,sequence):
        vlist = []
        for x in sequence:
            if isinstance(x,Cons): 
                if isinstance(x.car,Variable):
                    vlist.append(x.car)
                else:
                    vlist += self.get_variables(x.car)
                if isinstance(x.cdr,Variable):
                    vlist.append(x.cdr)
                else:
                    vlist += self.get_variables(x.cdr)
            elif type(x) == type((1, )) or type(x) == type([]):
                vlist += self.get_variables(x)
            elif isinstance(x,Variable):
                vlist.append(x)
            #if type(x) == type((1, )) or type(x) == type([]):
            #    vlist += self.get_variables(x)
            #elif isinstance(x,Variable):
            #    vlist.append(x)
        return vlist

    def tell(self, tuple):
        "Add the sentence to the KB"
        key = self.make_key(tuple)
        self.wm.setdefault(key,[]).append(tuple)

    def make_bc_rule(self,head, body):
        key = self.make_key(head)
        self.bcr.setdefault(key,[]).append((head,body))

    def make_fc_rule(self,head,body):
        self.fwr.append(FWRule(head,body))
        
    def ask(self, query, mores=True):
        """Ask returns a substitution that makes the query true, or
        it returns False. It is implemented in trems of ask_generator."""
        key = self.make_key(query)
        gvars = self.get_variables(query)
        iterator = self.wm[key].__iter__()
        try:
            unifier = Unify()
            printer = Printer()
            r = unifier.unify(iterator.next(),query,{})
            while True:
                if r: 
                    for x in gvars:
                        print x.name+": "+str(printer.deref(x,r))
                    # print r
                    if printer.query_yes_no("more solutions?","no")== "no":
                        return True
                r =  unifier.unify(iterator.next(),query,{})
        except StopIteration:
            return False

    def ask_generator(self, query):
        "Yield all the substitutions that make query true."
        abstract

    def retract(self, sentence):
        "Remove the sentence from the KB"
        abstract

    def makeResolvent(self, clausole, unificator):
        resolvent = ()

        for i in clausole:
            if str(i) in unificator:
                resolvent += (unificator[str(i)],)
            else:
                resolvent += (i,)

        return resolvent

    # Prove backward rules, if wm is True it also checks
    # ground facts in the wm.
    def prove(self, goals, wm=False):
        gvars = self.get_variables(goals)        
        if not self.bcprove(goals, {}, wm, gvars, 0):
            print "False"

# Schema for backward proof.
# bcprove(self,goals,env,wm,gvars,ret_fun)
# goals --> prolog query
# env
# wm --> bolean value, use or not use wm facts in the prove.
# gvars --> goal variables
# ret_fun --> function to return at the end (optional).


    def resolvetuple(self, goals, env, wm, gvars, level):
        

        #for goal in goals:
        goal = goals.pop(0)
        key = self.make_key(goal)
        iteratorBcr = self.bcr[key].__iter__()
        #kbRule = iteratorBcr.next()

        unifier = Unify()
        
        for kbRule in iteratorBcr:

            freshRule = copy.deepcopy(kbRule)
            frvars = self.get_variables(freshRule)

            print " > frvars=",self.printRule(frvars)
            
            for i in frvars:
                i.rename(level)

            print " > i=",self.printRule(kbRule[0])
            print " > j=",self.printRule(freshRule[0])
            print " > goal=",self.printRule(goal)
            print " > env=",self.printRule(env)
            print " > gvars=",self.printRule(gvars)

            newenv = {}
            newenv.update(env) #{}
            test = True

            for i in range(len(freshRule[0])):
                if type(goal[0]) == type((1, )):
                    q = unifier.unify(freshRule[0][i], goal[0][i], newenv)
                else:
                    q = unifier.unify(freshRule[0][i], goal[i], newenv)
                #q = unifier.unify(freshRule[0][i], goal[i], newenv) 
                #print self.printRule(q)
                if q is None:
                    test = False
                    #break
                else:
                    newenv.update(q)

            print " !> newenv=",self.printRule(newenv), "TEST",str(test)
            print ""
            
            if test:
                newgoals = copy.deepcopy(goals)
                
                print " !> freshRule[1]=",self.printRule(freshRule[1])
                
                if not isinstance(freshRule[1], bool):
                    newgoals.insert(0,freshRule[1])

                print " !> newgoals=",self.printRule(newgoals)
                # stdin.readline()

                if self.bcprove(newgoals, newenv, wm, gvars, level+1):
                    return True
                else:
                    print "BACKTRACK - level", level

        return False

    def bcprove(self,goals,env,wm,gvars,level):
        elements = []

        for goal in goals:    
            if type(goal[0]) == type((1, )):
                for tup in goal:
                    elements.append(tup)
            else:
                elements.append(goal)

        print "\n#", level, "#", elements

        if len(elements) == 0:
            printer = Printer()

            print "True\n"

            for x in gvars:
                #if isinstance(x, Variable):
                print x.name+": "+str(printer.deref(x, env))
            
            if printer.query_yes_no("more solutions?","no")== "no":
                return True
            else:
                return False

        return self.resolvetuple(elements,env,wm,gvars,level)

            # if result == None:
            #     test = False
            # elif isinstance(result, bool):
            #     return result
            # else:
            #     newenv.update(result)
            