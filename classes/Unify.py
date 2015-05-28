import operator

from Variable import Variable

class Unify:

    def unify(self, x, y, s):
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
            return self.unify_var(x, y, s)
        elif isinstance(y,Variable):
            return self.unify_var(y, x, s)
    #    elif isinstance(x, Expr) and isinstance(y, Expr):
    #        return self.unify(x.args, y.args, unify(x.op, y.op, s))
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
    #    elif occur_check(var, x):
    #        return None
        else:
            return self.extend(s, var.name, x)


    def extend(self, s, var, val):
        """Copy the substitution s and extend it by setting var to val; return copy.
        >>> extend({x: 1}, y, 2)
        {y: 2, x: 1}
        """
        s2 = s.copy()
        s2[var] = val
        return s2
