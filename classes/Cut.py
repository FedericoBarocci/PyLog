class Cut(object):

	class SingletonCut:
		def __init__(self):
			self.reached = False

		def __str__(self):
			return "reached" + str(self.reached)

	instance = None

	def __init__(self):
		if not Cut.instance:
			Cut.instance = Cut.SingletonCut()
	
	def reset(self): 
		Cut.instance.reached = False

	def set(self):
		Cut.instance.reached = True

	def test(self):
		return Cut.instance.reached

	def __str__(self):
		return str(Cut.instance)
