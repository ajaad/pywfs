
#print("Load: Hello world!")


class service:
    def __init__(self, hei):
        
        self.name = hei
        
    def __str__(self):
        
        return 'Navnet er {} i dag'.format(self.name)


def add_one(number):
    return number + 1