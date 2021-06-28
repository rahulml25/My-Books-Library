import os
import time
from typing import NoReturn


class Library(object):

    def __init__(self, name: str, register: dict) -> None:
        self.name = name
        self.register = register

    @classmethod
    def setup_library(cls, name: str, *books: tuple):
        register = cls.add_books({}, *books)
        return cls(name, register)

    def save_register(self):
        """
        saves the register as folder
        """
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
            book_data = data[book]
            lenders = ', '.join(book_data['lenders'])
            if lenders == '':
                lenders = None

            # Saving book data
            file = open(f'{folders}{book}.log', 'w')
            file.write(f"copy:{book_data['copy']};\n")
            file.write(f"lenders:{lenders}")
            file.close()

    @property
    def books(self) -> list:
        return list(self.register.keys())

    @property
    def available_books(self) -> list:
        return [book for book in self.books if self.book_availability(book) != 0]

    def book_availability(self, book: str) -> int:
        return self.register[book]["copy"]

    def book_lenders(self, book: str) -> list:
        return self.register[book]["lenders"]

    @property
    def lent_books(self) -> list:
        return [book for book in self.books if self.book_availability(book) == 0]

    @property
    def lenders(self) -> list:
        lenders = []
        for book in self.books:
            if self.book_availability(book) == 0:
                for lender in self.book_lenders(book):
                    lenders.append(lender)
        return lenders

    @staticmethod
    def add_books(main_register: dict, *books: tuple) -> dict:
        for book in books:
            if book[1] > 0:
                main_register[book[0]] = {"copy": book[1], "lenders": []}
            else:
                main_register[book[0]] = {"copy": book[1], "lenders": book[2]}
        return main_register

    @staticmethod
    def ask_to(sub: str) -> list or None:
        books = input(f"Enter the Books to {sub}:\n")
        print()
        if books == '':
            return None

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

    @staticmethod
    def ask_name() -> str or None:  # --- > for Python 3.10.0+
        name = input("Enter your name:\n").strip()
        print()
        if name == '':
            return None
        return name

    def print_lent_books(self) -> None:
        print("Lent Books are:")
        for book in self.lent_books:
            print(' ' * 3, f"{book}: {', '.join(self.book_lenders(book))}")
        print()

    def all_books(self) -> None:
        if len(self.available_books) != 0:
            print("Available Books are:")
            for book in self.available_books:
                print(' ' * 3, f"{book}: {self.book_availability(book)} copy")
        else:
            print("No books are available now!")
        print()

        if len(self.lent_books) != 0:
            self.print_lent_books()

    def lend_books(self) -> None:
        customer = self.ask_name()
        if customer is not None:
            books = self.ask_to("lend")
            if books is None:
                print("Sorry! your haven't entered any book(s) name.")
                return

        else:
            print("Sorry! your haven't entered your name.")
            return

        succeed = True
        for book in books:
            if book in self.available_books:
                self.register[book]["copy"] -= 1
                if customer not in self.register[book]["lenders"]:
                    self.register[book]["lenders"].append(customer)
            else:
                succeed = False
                print(f"Sorry! book '{book}' is not available.")
        if succeed:
            print("You successfully lent books")
        print()

    def donate_books(self) -> None:
        books = self.ask_to("donate")
        if books is None:
            print("Sorry! your haven't entered any book(s) name.")
            return

        for book in books:
            if book in self.available_books:
                self.register[book]["copy"] += 1
            else:
                self.register = self.add_books(self.register, (book, 1))
        print("You successfully donated books\n")
        print("Thank you! for donating books")
        print()

    def return_books(self) -> None:
        succeed = True
        if len(self.lent_books) != 0:
            customer = self.ask_name()
            if customer is None:
                print("Sorry! your haven't entered your name.")
                return None

        else:
            print("No books to return", end='')
            time.sleep(0.6), print('!', end='')
            time.sleep(1), print('')
            return None

        if customer in self.lenders:
            books = self.ask_to("return")
            for book in books:
                if book in self.lent_books:
                    if customer in self.register[book]["lenders"]:
                        self.register[book]["copy"] += 1
                        self.register[book]["lenders"].remove(customer)
                    else:
                        succeed = False
                        print(f"You haven't lent book '{book}'!")
                else:
                    succeed = False
                    print(f"This book '{book}' is not lent!")

        else:
            succeed = False
            print("You have not lent any books!")

        if succeed:
            print("You successfully returned books!\n")
            print("Thank you! for returning books")
            print()

    def run(self) -> NoReturn:
        print(f"Welcome to {self.name}:\n")
        while True:
            print("Use Following options:\n1. Available Books \n2. Lend Books \n3. Donate Books \n4. Return Books \n")
            choice = input("Enter your choice:\n\n:⏩ ").strip()
            print()

            if choice == "1":
                self.all_books()

            elif choice == "2":
                self.lend_books()

            elif choice == "3":
                self.donate_books()

            elif choice == "4":
                self.return_books()

            elif choice == "q":
                quit()

            self.save_register()
            print("." * 17)


if __name__ == "__main__":
    rahul = Library.setup_library(
        "RahulML2505-Library",
        ("Python", 0, ["Rahul", ]),
        ("Java", 1)
    )
    rahul.run()
