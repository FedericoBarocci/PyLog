import sys, getopt, imp

from lib import KB

from rules import rules
from tests import tests
#from rules import lists
#from tests import testlist

def main(argv):
	kb = KB()

	try:
		opts, args = getopt.getopt(argv,"r:i:",["rfile=","ifile="])
	except getopt.GetoptError:
		print 'Usage: -r <rulesfile> -i <definitionsfile>'
		sys.exit(2)
	
	defaultRules = True
	defaultIn = True

	for opt, arg in opts:
		if opt in ("-r", "--rfile"):
			defaultRules = False
			r = imp.load_source('__main__', arg)
		elif opt in ("-i", "--ifile"):
			defaultIn = False
			i = imp.load_source('__main__', arg)

	if defaultRules:
		rules.defrules(kb)
		#lists.defrules(kb)
	else:
		r.defrules(kb)

	print "[KB rules]"
	kb.printAllRules()

	#tests
	if defaultIn:
		tests.test(kb)
		#testlist.test(kb)
	else:
		i.test(kb)

if __name__ == '__main__':
	main(sys.argv[1:])