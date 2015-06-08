import string

def defrules(kb):
	kb.defvar('_')
	
	for var in string.uppercase:
		kb.defvar(var)
		kb.defvar(var+"1")

	kb.defsym("unify")

	(unify, X, X) |IF| True

	kb.defsym("member")
	kb.defsym("member_")

	(member_, _, E, E) |IF| True
	(member_, H|T, E, _) |IF| (member_, T, E, H)
	(member, E, H|T) |IF| (member_, T, E, H)

	kb.defsym("append")

	(append, [], X, X) |IF| True
	(append, X|T, Y, X|U) |IF| (append, T, Y, U)

	kb.defsym("reverse")

	(reverse, X1, Y1) |IF| (reverse, X1, [], Y1, Y1)
	(reverse, [], Y1, Y1, []) |IF| True
	(reverse, X|X1, R1, Y1, _|B) |IF| (reverse, X1, X|R1, Y1, B)

	kb.defsym("memberchk")

	(memberchk, X, []) |IF| (cut, False)
	(memberchk, X, X|T) |IF| (cut, True)
	(memberchk, Y, X|T) |IF| (memberchk, Y, T)

	kb.defsym("testu")

	(testu, X, [])  |IF| True
	(testu, X, X|T) |IF| (testu, X, T)

	kb.defsym("union")

	(union, [], L, L) |IF| (cut, True)
	(union, H|T, L, R) |IF| ((member, H, L), (cut, True), (union, T, L, R))
	(union, H|T, L, H|R) |IF| (union, T, L, R)