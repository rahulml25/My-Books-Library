from typing import Union
from undefined import function, null


class Customer:

    def __init__(self) -> None:
        self.books = list()

    @classmethod
    def askTo(cls, action: str):
        """
        Asks the input of books from the user
        and returns the list of the books
        """
        books = input(
            f"Enter the name of the book you want to {action}: ").strip()

        if books == 'q':
            pass
        elif ',' in books:
            cls.books = [book.strip() for book in books.split(',')]
        else:
            cls.books = [books]

        return cls.books, action


class Library:
    """
    A Simple Class to manage a Library
    """

    welcomeMsg: str = '''\n ====== Welcome to Central Library ======
        Please choose an option:
        1. List all the books
        2. Request a book
        3. Add/Return a book
        4. Exit the Library
        '''

    ################# Initializer Methods #################

    def __init__(self, library_name: str, initial_books: list, register: dict) -> None:
        """
        Initialises some property variable
        """
        # Initial Properties
        self.name: str = library_name
        self.initial_books: list = initial_books
        self.register: dict = register

        # Member Class
        self.customer = Customer

    @classmethod
    def set_properties(cls, library_name: str, book_list: list) -> 'Library':
        """
        Custom Initialiser
        """
        register = cls.addBooks(cls, book_list)
        return cls(library_name, book_list, register)

    ################### Linier Methods ###################

    def bookAvailability(self, book: str) -> int:
        """
        returns the count of the book available in library
        """
        return self.register[book]['copies']

    def bookLenders(self, book: str) -> list[str]:
        """
        returns the list of the lender in the book profile
        """
        return self.register[book]['lenders']

    ################## Property Methods ##################

    @property
    def books(self) -> list[str]:
        """
        returns the list of the total books
        """
        return list(self.register.keys())

    @property
    def availableBooks(self) -> list[str]:
        """
        returns the list of the available books in the Library
        """
        return [book for book in self.books if self.bookAvailability(book) > 0]

    @property
    def unreturnedBooks(self) -> list[str]:
        """
        returns the list of the lended books in the Library
        """
        return [book for book in self.books if self.bookAvailability(book) == 0]

    @property
    def lenders(self) -> list[str]:
        """
        returns a list of the book lenders
        """
        lenders = list()
        [lenders.extend(self.bookLenders(book))
         for book in self.unreturnedBooks]
        return lenders

    @property
    def p(self) -> None:
        """
        A empty function to replicate
        the code in future property functions
        """
        pass

    ################### Special Methods ###################

    def addBooks(self, books: list, main_register: dict = {}) -> bool:
        """
        Adds new books to the register
        """
        for book in books:
            main_register[book] = {}
            main_register[book]['copies'] = 1
            main_register[book]['lenders'] = []

    def processBooks(self, books: Union[list, str], action: str,
                     if_zero_books: function, else_in_for_loop: function,
                     books_check: property, books_to_add: int = 1, final_imp: function = null) -> bool:
        """
        A function template to make processes in the Library `register`
        """

        if len(books):
            print("Please enter the names of the books!")
            return if_zero_books(self.customer.askTo(action))

        elif books == 'q':
            return False

        for book in books:
            if book in books_check:
                self.register[book]['copies'] += books_to_add
            else:
                else_in_for_loop(book)

        final_imp()

    #################### Main Methods ####################

    def displayAvailableBooks(self, ):
        """
        Prints all the books available in the Library
        """
        print("Books present in this library are: ")
        for book in self.availableBooks:
            print(" *"+book)

    def borrowBooks(self, askToObj: tuple[list, str]) -> bool:
        """
        Helps to borrow books from the Customer
        """
        books, action = askToObj
        return self.processBooks(books, action,
                                 self.borrowBooks, lambda book: print(
                                     "Sorry, This book is either not available or has already been issued to someone else. Please wait until the book is available"),
                                 self.availableBooks, -1, lambda: print(
                                     f"You have been issued {', '.join(books)}. Please keep it safe and return it within 30 days")
                                 )

    def returnBooks(self, askToObj: tuple[list, str]) -> bool:
        """
        Adds books Donated/Returned by people
        """
        books, action = askToObj
        return self.processBooks(books, action,
                                 self.returnBooks, lambda book: self.addBooks(
                                     [book], self.register),
                                 self.unreturnedBooks
                                 )


if __name__ == "__main__":
    library = Library.set_properties(
        'Library',
        ['Python', 'Java']
    )

    while True:
        print(library.welcomeMsg)
        action = int(input("Enter a choice:⏩ "))

        if action == 1:
            library.displayAvailableBooks()
        elif action == 2:
            library.borrowBooks(
                library.customer.askTo('borrow')[0])
        elif action == 3:
            library.returnBooks(
                library.customer.askTo('donate'))
        elif action == 4:
            library.returnBooks(
                library.customer.askTo('return'))
        elif action == 5:
            print("Thanks for choosing Central Library. Have a great day ahead!")
            break
        else:
            print("Invalid Choice!")
