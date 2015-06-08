import string

class Infix:

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


class Cons(object):

	def __init__(self,car,cdr):
		self.car = car
		self.cdr = cdr

	def __str__(self):
		return "["+str(self.car)+"|"+str(self.cdr)+ "]"


class Symbol(object):

	LogicalOperators = ["AND","OR","IF","IFF","NOT"]

	def __init__(self,name):
		self.name = name

	def __repr__(self):
		return self.name

	def __or__(self, other):
		return Cons(self,other)


class Variable(Symbol):

	def __init__(self,name): 
		if name[0] in string.lowercase:
			raise TypeError("Variables begins with Uppercase letters")
		elif name in Symbol.LogicalOperators:
			raise TypeError("This is a logical operator")
		else:
			Symbol.__init__(self,name)
			self.sname = name

	def __str__(self):
		return self.name

	def __eq__(self,Var):
		return (isinstance(Var,Variable) and self.name == Var.name)

	def deref(self,env):
		if env.has_key(self.name):
			return deref(env[self.name],env)
		else:
			return self.name
	
	def rename(self,n):
		self.name = "_"+self.sname+str(n)


class FSymbol(Symbol):
	
	def __init__(self,name):
		if name[0] in string.uppercase:
			raise TypeError("FSymbols begins with lowercase letters")
		elif name in Symbol.LogicalOperators:
			raise TypeError("This is a logical operator")
		else:
			Symbol.__init__(self,name)

	def __cmp__(self,other):
		return self.name != other.name