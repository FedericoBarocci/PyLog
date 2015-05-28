class Cons():
    
    def __init__(self,car,cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return "["+str(self.car)+"|"+str(self.cdr)+ "]"
