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
            if type(x) == type((1, )) or type(x) == type([]):
                vlist += self.get_variables(x)
            elif isinstance(x,Variable):
                vlist.append(x)
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
        #resolvent = clausole
        resolvent = ()
        print clausole
        print unificator
        print resolvent

        for i in clausole:
            

            if str(i) in unificator:
                print i,"in",unificator
                resolvent += (unificator[i],)
            else:
                print i,"not in",unificator
                resolvent += (str(i),)

            print resolvent
            # resolvent[i] = clausole[0][i]
            # print resolvent[i]
            # for j in unificator:
            #     if i == j:
            #         resolvent[i] = unificator[j]

        print "resolvent=",self.printRule(resolvent)

        return resolvent

    # Prove backward rules, if wm is True it also checks
    # ground facts in the wm.
    def prove(self, goals, wm=False):
        gvars = self.get_variables(goals)        
        self.bcprove(goals, {}, wm, gvars)

# Schema for backward proof.
# bcprove(self,goals,env,wm,gvars,ret_fun)
# goals --> prolog query
# env
# wm --> bolean value, use or not use wm facts in the prove.
# gvars --> goal variables
# ret_fun --> function to return at the end (optional).
    def bcprove(self,goals,env,wm,gvars):
        #iteratorGoals = goals.__iter__()
        print goals

        for goal in goals: #[(append, [1,2],[3],X)]:
        #try:
            #while True:
                #goal = iteratorGoal.next()

            key = self.make_key(goal)

            iteratorBcr = self.bcr[key].__iter__()
            try:
                while True:
                    unifier = Unify()
                    i = iteratorBcr.next()

                    print " > i=",self.printRule(i[0])
                    print " > goal=",self.printRule(goal)
                    print " > env=",self.printRule(env)
                    

                    newenv = {}
                    test = True
                    for j in range(len(i[0])):
                        q = unifier.unify(i[0][j], goal[j], env) 
                        
                        if q is None:
                            test = False
                            #break
                        else:
                            newenv.update(q)

                    print " !> newenv=",self.printRule(newenv), "TEST",str(test)
                    print ""
                    
                    if test:
                        #if not(None in newenv):
                            #TODO capire come scrivere questa parte
                            #newenv = {}
                            #for x in r:
                            #    for xi in x:
                            #        newenv[xi] = x[xi]

                        self.bcprove([self.makeResolvent(i[1], newenv)], newenv, wm, self.get_variables(goals))
            except StopIteration:
                #fail
                print "StopIteration\n"
                return False
        
        #except StopIteration:
            #success
        
        print "bcprove endfor\n"

        printer = Printer()

        for x in gvars:
            #r = Unifier.unify(x, )
            print x.name+": "#+str(printer.deref(x,r))
        
        if printer.query_yes_no("more solutions?","no")== "no":
            return True

#        return True