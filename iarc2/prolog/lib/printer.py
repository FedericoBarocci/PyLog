import sys

from structs import Variable, Cons

class Printer:

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

	def printRule(self, element):
		if element is None:
			return str(None)
		elif isinstance(element, str) or isinstance(element, int) or isinstance(element, bool):
			return str(element)
		elif isinstance(element, Variable):
			return element.__str__()
		elif (isinstance(element,Cons)):
			return " | ".join( [ self.printRule(element.car), self.printRule(element.cdr) ])

		list = []
		
		if type(element) is type([]):
			for i in element:
				list.append(self.printRule(i))
			return "[" + ", ".join(list) + "]"

		if type(element) is type({}):
			for i in element:
				list.append( self.printRule(i) + " : " + self.printRule(element[i]) )
			return "{" + ", ".join(list) + "}"

		for i in element:
			if (isinstance(i,Cons)):
				list.append( " | ".join( [ self.printRule(i.car), self.printRule(i.cdr) ]))
			elif type(i) is type((1, )):
				list.append(str(self.printRule(i)))
			else:
				list.append(str(i))

		return "(" + ", ".join(list) + ")"