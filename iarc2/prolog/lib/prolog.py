import string
import operator
import sys
import copy
import __builtin__

from structs import Variable, FSymbol, Cons
from printer import Printer
from cut import Cut

sys.setrecursionlimit(1000000000)

class Unify:

	def unify(self, x, y, s):
		if s == None:
			return None
		elif x == y:
			return s
		elif isinstance(x,Variable):
			return self.unify_var(x, y, s)
		elif isinstance(y,Variable):
			return self.unify_var(y, x, s)
		elif isinstance(x, str) or isinstance(y, str) or not x or not y:
			if (x == y):
				return s
			else:
				return None
		elif operator.isSequenceType(x) and operator.isSequenceType(y) and len(x) == len(y):
			return self.unify(x[1:], y[1:], self.unify(x[0], y[0], s))
		elif isinstance(x,Cons) and isinstance(y,Cons):
			return self.unify(x.cdr, y.cdr, self.unify(x.car, y.car, s))
		elif isinstance(x,Cons) and operator.isSequenceType(y) and len(y) == 1:
			return self.unify(x.cdr, [], self.unify(x.car, y[0], s))
		elif isinstance(x,Cons) and operator.isSequenceType(y):
			return self.unify(x.cdr, y[1:], self.unify(x.car, y[0], s))
		elif isinstance(y,Cons) and operator.isSequenceType(x) and len(x) == 1:
			return self.unify(y.cdr, [], self.unify(y.car, x[0], s))
		elif isinstance(y,Cons) and operator.isSequenceType(x):
			return self.unify(y.cdr, x[1:], self.unify(y.car, x[0], s))
		else:
			return None

	def unify_var(self, var, x, s):
		if var.name in s:
			return self.unify(s[var.name], x, s)
		else:
			return self.extend(s, var.name, x)

	def extend(self, s, var, val):
		s2 = s.copy()
		s2[var] = val

		return s2


class KB:

	__kb__ = "empty"

	def __init__(self):
		self.wm = {}
		self.bcr = {}
		self.fwr = []
		self.fwrnodes = {}
		KB.__kb__ = self

		self.defsym("cut")

	def defvar(self, var):
		command = "__builtin__."+var+"=Variable('"+var+"')"
		exec command

	def defsym(self, sym):
		command = "__builtin__."+sym+"=FSymbol('"+sym+"')"
		exec command

	def make_key(self,tuple):
		return str(tuple[0])+str(len(tuple)-1)

	def printAllRules(self):
		for key in self.bcr:
			for element in self.bcr[key]:
				#print " ", Printer().deref(element[0], {}), ":-", str(Printer().deref(element[1], {})) + "."
				print " ", Printer().printRule(element[0]), ":-", str(Printer().printRule(element[1])) + "."
		
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

		return vlist

	def tell(self, tuple):
		key = self.make_key(tuple)
		self.wm.setdefault(key,[]).append(tuple)

	def make_bc_rule(self,head, body):
		if head != "cut":
			key = self.make_key(head)
			self.bcr.setdefault(key,[]).append((head,body))

	def make_fc_rule(self,head,body):
		self.fwr.append(FWRule(head,body))
		
	def ask(self, query, mores=True):
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

					if printer.query_yes_no("more solutions?","no")== "no":
						return True

				r =  unifier.unify(iterator.next(),query,{})
		except StopIteration:
			return False

	def ask_generator(self, query):
		abstract

	def retract(self, sentence):
		abstract

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