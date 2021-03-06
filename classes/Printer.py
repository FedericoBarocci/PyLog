import sys

from Variable import Variable
from Cons import Cons

class Printer:

    # dereference
    def deref(self,var,env):
        if isinstance(var, Variable) and var.name in env:
          return self.deref(env[var.name],env)
        elif isinstance(var,Cons):
            tail = self.deref(var.cdr,env)
            if type(tail) == type([]):
                return [self.deref(var.car,env)]+tail
            else:
                return [self.deref(var.car,env)]+[tail]
        elif type(var) == type((1, )):
            return self.deref_tuple(var,env)
        elif type(var) == type([]):
            return self.deref_list(var,env)
        else:
            return var
        

    def deref_list(self,list,env):
        newlist = []
        for x in list:
            if type(x) == type((1, )):
                newlist.append(self.deref_tuple(x,env))
            elif type(x) == type([]):
                newlist.append(self.deref_list(x,env))
    #        elif isinstance(x,Variable) and x.name in env:
    #            newlist.append(deref(env[x.name],env))
            else:
                newlist.append(self.deref(x,env))
        return newlist

    def deref_tuple(self,tuple,env):
        newtuple = ()
        for x in tuple:
            if type(x) == type((1, )):
                newtuple += (self.deref_tuple(x,env),)
            elif type(x) == type([]):
                newtuple += (self.deref_list(x,env),)
            else:
                newtuple += (self.deref(x,env),)
        return newtuple

    def print_args_and_return_env(self,gvars,env):
        for x in gvars:
            print x.name+": "+str(self.deref(x,env))
        if self.query_yes_no("more solutions?","no") == "no":
            return env
        else:
            return False


    def query_yes_no(self,question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.
        
        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":"yes", "y":"yes", "ye":"yes", "no":"no", "n":"no"}

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
                sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")