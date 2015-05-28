# import ai_module
import ai

kb=ai.init()

# defining symbols used in rules
ai.defsym("m")
ai.defsym("k")
ai.defsym("append")
ai.defsym("testu")
ai.defsym("unify")
ai.defsym("member")
ai.defsym("union")
ai.defsym("appendt")
ai.defsym("reverse")
ai.defconcept("person")


# use of ask & tell interface
kb.tell((m, 1,2))
kb.tell((m, 3,4))
kb.tell((m, [1,2], [3,4]))


kb.ask((m, X,Y))

# definition of rules:

(k, X, Y) |IF| (m, Y, X)

(unify, X, X) |IF| True

(append, [], X, X) |IF| True
(append, X|T, Y, X|U) |IF| (append, T, Y, U)

(reverse, [], []) |IF| True
(reverse, X|T, Y) |IF| ((reverse, T, U),(append, U, [X], Y))

(member, X, X|T) |IF| True
(member, Y, X|T) |IF| (member, Y, T)

(testu, X, [])  |IF| True
(testu, X, X|T) |IF| (testu, X, T)

(union,[],X,X) |IF| True
(union, H|T,X,U) |IF| ((member,H,X),(union,T,X,U))
(union, H|T,S,H|U) |IF| (union,T,S,U)

print kb.bcr

#tests
#kb.prove([(append, [1,2],[3],X)])
#kb.prove([(append, X, Y, [1,2,3])])
#kb.prove([(member, X, [1,2,3,5,6])])
#kb.prove([(reverse, [1,2,3,5,6],X)])
#kb.prove([(reverse, X, [1,2,3,5,6])])
#kb.prove([(testu, Y, [1,2,3])])
#kb.prove([(union, [2,3,7,8], [1,2,3,4,5,6], X)])





 
