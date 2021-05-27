import os

class Library(object):
    
    def __init__(self,name,register):
        self.name = name
        self.register = register
        self.books = self.register.keys()

    def funcname(self, parameter_list):
        pass