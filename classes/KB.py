from Variable import Variable
from Printer import Printer
from FSymbol import FSymbol
from Unify import Unify

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

                    print "i=",i," goal=",goal

                    r = unifier.unify(i, goal, env) 

                    print "r=",r,"\n"
                    
                    if r == None:
                        return False 

                    #TODO capire come scrivere questa parte
                    self.bcprove(self, goals.remove(goal), env.append(r), wm, self.get_variables(goals))
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