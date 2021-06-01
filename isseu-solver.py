import os

class Library(object):

    def __init__(self, name, register):
        self.name = name
        self.register = register

    @classmethod
    def setup_library(cls, name, *books):
        register = cls.addBooks(cls, {}, *books)
        return cls(name, register)

    @property
    def books(self):
        return self.register.keys()

    @property
    def availableBooks(self):
        return [book for book in self.books if self.bookAvailability(book)!=0]

    def bookAvailability(self, book):
        return self.register[book]["copy"]

    def bookLenders(self, book):
        return self.register[book]["lenders"]

    @property
    def lendedBooks(self):
        return [book for book in self.books if self.bookAvailability(book)==0]

    @property
    def lenders(self):
        return [lender for lender in self.lenders(book) for book in self.books if self.bookAvailability(book)==0]

    def addBooks(self, main_register, *books):
        for book in books:
            if book[1]>0:
                main_register[book[0]] = {"copy": book[1], "lenders": []}
            else:
                main_register[book[0]] = {"copy": book[1], "lenders": book[2]}
        return main_register

    def askTo(self, sub):
        books = input(f"Enter Books to {sub}:\n")
        if ', ' in books:
            books = books.split(', ')
        elif ',' in books:
            books = books.split(',')
        elif ' and ' in books:
            books = books.split(' and ')
        else:
            book = books
            return [book]
        return books

    def printLendedBooks(self):
        print("Lended Books are:")
        for book in self.lendedBooks:
            print(' '*3,f"{book}: {', '.join(self.bookLenders(book))}")
        print()

    def allBooks(self):
        if len(self.availableBooks)!=0:
            print("Available Books are:")
            for book in self.availableBooks:
                print(' '*3,f"{book}: {self.bookAvailability(book)} copy")
        else:
            print("No books are available now!")
        print()
        self.printLendedBooks()

    def lendBooks(self):
        customer = input("Ener your name:\n"),print()
        books = self.askTo("lend")
        print()
        succedd = True
        for book in books:
            if book in self.availableBooks:
                self.register[book]["copy"] -= 1
                if not customer in self.register[book]["lenders"]:
                    self.register[book]["lenders"].append(customer)
            else:
                succedd = False
                print(f"Sorry! book '{book}' is not available.")
        if succedd:
            print("You sucessfully lended books\n")
        print()

    def donateBooks(self):
        books = self.askTo("donate")
        print()
        for book in books:
            if book in self.availableBooks:
                self.register[book]["copy"] += 1
            else:
                self.register = self.addBooks(self.register, (book, 1))
        print("You sucessfully donated books\n")
        print("Thank you! for donating books")
        print()

    def returnBooks(self):
        succeed = True
        customer = input("Ener your name:\n"),print()
        if customer in self.lenders:
            books = self.askTo("return")
            for book in books:
                if book in self.lendedBooks:
                    if customer in self.register[book]["lenders"]:
                        self.register[book]["copy"] += 1
                        self.register[book]["lenders"].remove(customer)
                    else:
                        succeed = False
                        print(f"You haven't lended book '{book}'!")
                else:
                    succeed = False
                    print(f"This book '{book}' is not lended!")
        else:
            succeed = False
            print("You have not lended any books!")
        
        if succeed:
           print("You sucessfully returned books\n")
           print("Thank you! for returning books")
           print() 

    def run(self):
        print(f"Welcome to {self.name}:\n")
        while True:
            print("Use Following options:\n1. Available Books \n2. Lend Books \n3. Donate Books \n4. Return Books \n")
            choice = input("Enter your choice:\n\n:⏩ ").strip()
            print()
            
            if choice=="1":
                self.allBooks()
    
            elif choice=="2":
                self.lendBooks()
    
            elif choice=="3":
                self.donateBooks()
    
            elif choice=="4":
                self.returnBooks()
            print(".............\n............\n")

if __name__ == "__main__":
    rahul = Library.setup_library(
        "RahulML2505-Library",
        ("Python", 0, ["Rahul",]),
        ("Java", 1)
        )
    rahul.run()