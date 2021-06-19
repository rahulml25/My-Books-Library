import os, time
from typing import NoReturn

class Library(object):

    def __init__(self, name: str, register: dict) -> None:
        self.name = name
        self.register = register

    @classmethod
    def setup_library(cls, name: str, *books: tuple):
        register = cls.addBooks(cls, {}, *books)
        return cls(name, register)

    def saveRegister(self):
        ''' saves the register as folder '''
        register = 'register\\'
        folders = r'register\data\\'
        
        # Creating Folder if doesn't exists
        if not os.path.exists(folders):
        	os.makedirs(folders)

        # Saving names of the books
        books = self.books

        with open(f"{register}books.log", 'w') as file:
            file.write(f"{', '.join(books)}")
        
        # Saving data for all books
        data = self.register
        for book in books:
            Book = data[book]
            lenders = ', '.join(Book['lenders'])
            if lenders == '': lenders = None

            # Saving book data
            file = open(f'{folders}{book}.log', 'w')
            file.write(f"copy:{Book['copy']};\n"); file.write(f"lenders:{lenders}")
            file.close()

    @property
    def books(self) -> list:
        return list(self.register.keys())

    @property
    def availableBooks(self) -> list:
        return [book for book in self.books if self.bookAvailability(book)!=0]

    def bookAvailability(self, book: str) -> int:
        return self.register[book]["copy"]

    def bookLenders(self, book: str) -> list:
        return self.register[book]["lenders"]

    @property
    def lendedBooks(self) -> list:
        return [book for book in self.books if self.bookAvailability(book)==0]

    @property
    def lenders(self) -> list:
        lenders = []
        for book in self.books:
            if self.bookAvailability(book)==0:
                for lender in self.bookLenders(book):
                    lenders.append(lender)
        return lenders

    def addBooks(self, main_register: dict, *books: tuple) -> dict:
        for book in books:
            if book[1]>0:
                main_register[book[0]] = {"copy": book[1], "lenders": []}
            else:
                main_register[book[0]] = {"copy": book[1], "lenders": book[2]}
        return main_register

    def askTo(self, sub: str) -> list | None:
        books = input(f"Enter the Books to {sub}:\n"); print()
        if books=='':
            return None

        if ', ' in books:
            books = books.split(', ')
        elif ',' in books:
            books = books.split(',')
        elif ' and ' in books:
            books = books.split(' and ')
        else:
            book = books; return [book]
        return books

    def askName(self) -> str | None: #--- > for Python 3.10.0+
        name = input("Enter your name:\n").strip(); print()
        if name=='':
            return None
        return name

    def printLendedBooks(self) -> None:
        print("Lended Books are:")
        for book in self.lendedBooks:
            print(' '*3,f"{book}: {', '.join(self.bookLenders(book))}")
        print()

    def allBooks(self) -> None:
        if len(self.availableBooks)!=0:
            print("Available Books are:")
            for book in self.availableBooks:
                print(' '*3,f"{book}: {self.bookAvailability(book)} copy")
        else:
            print("No books are available now!")
        print()

        if len(self.lendedBooks)!=0:
            self.printLendedBooks()

    def lendBooks(self) -> None:
        customer = self.askName()
        if customer!=None:
            books = self.askTo("lend")
            if books==None:
                print("Sorry! your haven't entered any book(s) name.")
                return None
        else:
            print("Sorry! your haven't entered your name.")
            return None
        
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

    def donateBooks(self) -> None:
        books = self.askTo("donate")
        if books==None:
            print("Sorry! your haven't entered any book(s) name.")
            return None
        
        for book in books:
            if book in self.availableBooks:
                self.register[book]["copy"] += 1
            else:
                self.register = self.addBooks(self.register, (book, 1))
        print("You sucessfully donated books\n")
        print("Thank you! for donating books")
        print()

    def returnBooks(self) -> None:
        succeed = True
        if len(self.lendedBooks)!=0:
            customer = self.askName()
            if customer==None:
                print("Sorry! your haven't entered your name.")
                return None

        else:
            print("No books to return", end=''); time.sleep(0.6), print('!', end=''); time.sleep(1), print('')
            return None

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
           print("You sucessfully returned books!\n")
           print("Thank you! for returning books")
           print()

    def run(self) -> NoReturn:
        print(f"Welcome to {self.name}:\n")
        while True:
            print("Use Following options:\n1. Available Books \n2. Lend Books \n3. Donate Books \n4. Return Books \n")
            choice = input("Enter your choice:\n\n:⏩ ").strip(); print()

            if choice=="1":
                self.allBooks()

            elif choice=="2":
                self.lendBooks()

            elif choice=="3":
                self.donateBooks()

            elif choice=="4":
                self.returnBooks()

            elif choice=="q":
                quit()

            self.saveRegister()
            print("."*17)

if __name__ == "__main__":
    rahul = Library.setup_library(
        "RahulML2505-Library",
        ("Python", 0, ["Rahul",]),
        ("Java", 1)
        )
    rahul.run()