def test(kb):
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