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

    @property
    def books(self) -> None:
        return self.register.keys()

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
        return [(lender for lender in self.bookLenders(book)) for book in self.books if self.bookAvailability(book)==0]

    def addBooks(self, main_register: dict, *books: tuple) -> dict:
        for book in books:
            if book[1]>0:
                main_register[book[0]] = {"copy": book[1], "lenders": []}
            else:
                main_register[book[0]] = {"copy": book[1], "lenders": book[2]}
        return main_register

    def askTo(self, sub: str) -> list:
        books = input(f"Enter Books to {sub}:\n")
        if ', ' in books:
            books = books.split(', ')
        elif ',' in books:
            books = books.split(',')
        elif ' and ' in books:
            books = books.split(' and ')
        else:
            book = books; return [book]
        return books

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

    def donateBooks(self) -> None:
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

    def returnBooks(self) -> None:
        succeed = True
        if len(self.lendedBooks) != 0:
            customer = input("Ener your name:\n"); print()
        else:
            print("No books to return", end=''); time.sleep(0.6), print('!', end='')
            time.sleep(1) , print(''); return None

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
            
            print("."*17)

if __name__ == "__main__":
    rahul = Library.setup_library(
        "RahulML2505-Library",
        # ("Python", 0, ["Rahul",]),
        ("Java", 1)
        )
    rahul.run()
    # print(rahul)