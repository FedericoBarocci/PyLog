import copy

from Variable import Variable
from Printer import Printer
from FSymbol import FSymbol
from Unify import Unify
from Cons import Cons
from Cut import Cut

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

    def printAllRules(self):
        for key in self.bcr:
            for element in self.bcr[key]:
                print " ", Printer().deref(element[0], {}), ":-", str(Printer().deref(element[1], {})) + "."
        
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
        if head == "cut":
            return

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
    def prove(self, goals):
        print "?-", Printer().deref(goals,{})
        
        Cut().reset()
        gvars = self.get_variables(goals)
        result = self.bcprove(goals, {}, gvars, 0)

        print Printer().deref(result,{}), "\n"

        return result

    def solve(self, goals, env, gvars, level):
        goal = goals.pop(0)

        if isinstance(goal, bool):
            return self.bcprove(goals, env, gvars, level+1)
        elif isinstance(goal, tuple) and goal[0].name is "cut":
            goals.insert(0, goal[1])
            result = self.bcprove(goals, env, gvars, level+1)
            Cut().set()
            return result

        key = self.make_key(goal)
        iteratorBcr = self.bcr[key].__iter__()
        
        for kbRule in iteratorBcr:
            freshRule = copy.deepcopy(kbRule)
            freshvars = self.get_variables(freshRule)
            
            for i in freshvars:
                i.rename(level)

            newenv = {}
            newenv.update(env)
            test = True

            for i in range(len(freshRule[0])):
                q = Unify().unify(freshRule[0][i], goal[i], newenv)

                if q is None:
                    test = False
                    break
                else:
                    newenv.update(q)
            
            if test:
                newgoals = copy.deepcopy(goals)
                newgoals.insert(0, freshRule[1])
                result = self.bcprove(newgoals, newenv, gvars, level+1)

                if Cut().test() or result:
                    return result

        return False

    def bcprove(self,goals,env,gvars,level):
        elements = []

        for goal in goals:
            if isinstance(goal, bool):
                elements.append(goal)
            elif type(goal[0]) == type((1, )):
                for tup in goal:
                    elements.append(tup)
            else:
                elements.append(goal)

        if len(elements) == 1 and isinstance(elements[0], bool):
            if not elements[0]:
                return False
            
            print elements[0]

            for x in gvars:
                print x.name+": "+str(Printer().deref(x, env))
            
            return Printer().query_yes_no("more solutions?","no") == "no"

        return self.solve(elements,env,gvars,level) 