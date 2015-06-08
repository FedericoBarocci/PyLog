import string
import operator
import sys
import __builtin__

sys.path.append('./classes')

import Infix
import BSymbol
import Cons
import Symbol
import Variable
import Printer
import FSymbol
import LOperator
import Unify
import KB
import Initializer

kb = Initializer.init()

Initializer.defsym("m")
Initializer.defsym("k")
Initializer.defsym("cut")
Initializer.defsym("append")
Initializer.defsym("testu")
Initializer.defsym("unify")
Initializer.defsym("member")
Initializer.defsym("member_")
Initializer.defsym("memberchk")
Initializer.defsym("union")
Initializer.defsym("reverse")
#Initializer.defconcept("person")

# use of ask & tell interface
kb.tell((m, 1,2))
kb.tell((m, 3,4))
kb.tell((m, [1,2], [3,4]))

#kb.ask((m, X,Y))

# (cut, X) |IF| True

(k, X, Y) |IF| (m, Y, X)

(unify, X, X) |IF| True

(append, [], X, X) |IF| True
(append, X|T, Y, X|U) |IF| (append, T, Y, U)

#(reverse, [], []) |IF| True
#(reverse, X|T, Y) |IF| ((reverse, T, U),(append, U, [X], Y))

(reverse, X1, Y1) |IF| (reverse, X1, [], Y1, Y1)
(reverse, [], Y1, Y1, []) |IF| True
(reverse, X|X1, R1, Y1, _|B) |IF| (reverse, X1, X|R1, Y1, B)


(member_, _, E, E) |IF| True
(member_, H|T, E, _) |IF| (member_, T, E, H)
(member, E, H|T) |IF| (member_, T, E, H)


(memberchk, X, []) |IF| (cut, False)
(memberchk, X, X|T) |IF| (cut, True)
(memberchk, Y, X|T) |IF| (memberchk, Y, T)

(testu, X, [])  |IF| True
(testu, X, X|T) |IF| (testu, X, T)

# (union,[],X,X) |IF| True
# (union, H|T,X,U) |IF| ((member,H,X),(union,T,X,U))
# (union, H|T,S,H|U) |IF| (union,T,S,U)

(union, [], L, L) |IF| (cut, True)
(union, H|T, L, R) |IF| ((member, H, L), (cut, True), (union, T, L, R))
(union, H|T, L, H|R) |IF| (union, T, L, R)

#print kb.bcr

print "[KB rules]"
kb.printAllRules()

#tests


kb.prove([(memberchk, 3, [1,2,3,3,3,3])])
kb.prove([(memberchk, 3, [1,2,3,4,5,6])])

kb.prove([(append, [1], [2], X)])
kb.prove([(append, [1,2],[3],X)])
kb.prove([(append, X, Y, [1,2,3])])
kb.prove([(member, 8, [1,2,3,5,6])])
kb.prove([(member, X, [1,2,3,4,5,6])])
kb.prove([(reverse, [1,2,3,5,6],X)])
kb.prove([(reverse, [1,2,3],X)])
kb.prove([(reverse, X, [1,2,3,5,6])])
kb.prove([(reverse, X, [1])])
kb.prove([(testu, Y, [1,2,3])])
kb.prove([(testu, Y, [1,1,1])])
kb.prove([(union, [2,3,7,8], [1,2,3,4,5,6], X)])
kb.prove([(union, [1], [2], X)])