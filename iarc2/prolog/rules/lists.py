import string

# Based on subset of SWI-Prolog implementation of lists manipulation.
# For the original rules see /usr/lib/swi-prolog/library/lists.pl
def defrules(kb):
	kb.defvar('_')
	
	for var in string.uppercase:
		kb.defvar(var)
		kb.defvar(var+"0")
		kb.defvar(var+"1")

	kb.defsym("unify")

	(unify, X, X) |IF| True


	kb.defsym("memberchk")

	(memberchk, X, []) |IF| (cut, False)
	(memberchk, X, X|T) |IF| (cut, True)
	(memberchk, Y, X|T) |IF| (memberchk, Y, T)


	kb.defsym("member")
	kb.defsym("member_")

	(member_, _, E, E) |IF| True
	(member_, H|T, E, _) |IF| (member_, T, E, H)
	(member, E, H|T) |IF| (member_, T, E, H)


	kb.defsym("append")

	(append, [], X, X) |IF| True
	(append, X|T, Y, X|U) |IF| (append, T, Y, U)


	kb.defsym("prefix")

	(prefix, [], _) |IF| True
	(prefix, E|T0, E|T) |IF| (prefix, T0, T)


	kb.defsym("select")
	kb.defsym("select_")

	(select, X, X|T, T) |IF| True
	(select, E, H|T, H|R) |IF| (select, E, T, R)

	(select, X, X1, Y, Y1) |IF| (select_, X1, X, Y, Y1)
	(select_, X|L, X, Y, Y|L) |IF| True
	(select_, X0|X1, X, Y, X0|Y1) |IF| (select_, X1, X, Y, Y1)


	kb.defsym("selectchk")

	(selectchk, E, L, R) |IF| ((select, E, L, R0), (cut, True), (unify, R, R0))

	(selectchk, X, X1, Y, Y1) |IF| ((select, X, X1, Y, Y1), (cut, False))


	kb.defsym("last")
	kb.defsym("last_")

	(last, X|X1, L) |IF| (last_, X1, X, L)
	(last_, [], L, L) |IF| True
	(last_, X|X1, _, L) |IF| (last_, X1, X, L)


	kb.defsym("same_length")

	(same_length, [], []) |IF| True
	(same_length, _|T1, _|T0) |IF| (same_length, T1, T0)


	kb.defsym("reverse")

	(reverse, X1, Y1) |IF| (reverse, X1, [], Y1, Y1)
	(reverse, [], Y1, Y1, []) |IF| True
	(reverse, X|X1, R1, Y1, _|B) |IF| (reverse, X1, X|R1, Y1, B)


	kb.defsym("intersection")

	(intersection, [], _, []) |IF| (cut, True)
	(intersection, X|T, L, I) |IF| ((member, X, L), (cut, True), (unify, I, X|R), (intersection, T, L, R))
	(intersection, _|T, L, R) |IF| (intersection, T, L, R)


	kb.defsym("union")

	(union, [], L, L) |IF| (cut, True)
	(union, H|T, L, R) |IF| ((member, H, L), (cut, True), (union, T, L, R))
	(union, H|T, L, H|R) |IF| (union, T, L, R)


	kb.defsym("subset")

	(subset, [], _) |IF| (cut, True)
	(subset, E|R, S) |IF| ((member, E, S), (subset, R, S))


	kb.defsym("subtract")
	
	(subtract, [], _, []) |IF| (cut, True)
	(subtract, E|T, D, R) |IF| ((member, E, D), (cut, True), (subtract, T, D, R))
	(subtract, H|T, D, H|R) |IF| (subtract, T, D, R)
