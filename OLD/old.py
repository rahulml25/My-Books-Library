import os


class Library:
    """
    A simple Class to manage a Library
    """

    def __init__(self, library_name, initial_books, register):
        """
        Initialises some variable
        """
        self.name = library_name
        self.initial_books = initial_books
        self.register = register

    @classmethod
    def set_properties(cls, library_name, book_list):
        """
        Custom Initialiser
        """
        register = cls.addBook(cls, {}, book_list)
        return cls(library_name, book_list, register)

    @property
    def books(self):
        """
        returns the list of the total books
        """
        return list(self.register.keys())

    def availablity(self, book):
        """
        returns the number of copies of the given book
        """
        return int(self.register[book]['copy'])

    @property
    def lenders(self):
        """
        returns a list of the lenders
        """
        lenders = []
        for book in self.books:
            lender = self.register[book]['lender']
            if not lender == []:
                for l in lender:
                    lenders.append(l)
        return lenders

    @property
    def unreturnedBooks(self):
        """
        returns a list of the unreturned books
        """
        books = []
        for book in self.books:
            copy = self.register[book]['copy']
            if copy <= 0:
                books.append(book)
        return books

    def askTo(self, type):
        """
        returns inputing name(s) of the books
        """
        books = input(f'\nWhich book do you to {type}?\nEnter Books: ').strip()
        conditions = [', ', ',', ' and ']
        if ', ' in books or ',' in books or ' and ' in books:
            if ', ' in books:
                return books.split(', ')
            elif ',' in books:
                return books.split(',')
            elif ' and ' in books:
                return books.split(' and ')
        elif books == '':
            print(f'\nYou have not {type} any books!')
            return ['']
        else:
            return [books]

    def addBook(self, mainReg, books):
        """
        Helps adding books [returns a dictionary of books]
        """
        register = mainReg
        for book in books:
            register[book] = {}
            register[book]['copy'], register[book]['lender'] = 1, []
        return register

    def saveRegister(self):
        """
        saves the register as folder
        """
        folder = 'register/'
        if not os.path.exists(folder):
            os.mkdir(folder)
        books = self.books
        with open('register/books.txt', 'w') as f:
            f.write(f"{', '.join(books)}")
        data = self.register
        for book in books:
            svB = data[book]
            f = open(f'register/{book}.txt', 'w')
            f.write(f"copy:{svB['copy']}, \n")
            lenders = ', '.join(svB['lender'])
            if lenders == '':
                lenders = 'None'
            f.write(f"lender:{lenders}")
            f.close()

    def doing(self, work):
        print(f'\n{work.capitalize()} Books...')

    def wish(self, type, book_count):
        print(f'You successfully {type} the {book_count}!')

    def allBooks(self):
        print('\nBooks now available are:')
        for book in self.books:
            print(f"{1*' '}{book} : {self.register[book]['copy']} copy")
        self.print_unreturned('showing')

    def print_unreturned(self, type):
        books = self.unreturnedBooks
        if not books == []:
            print('\nThe unreturned books are: ', end='')
            if type == 'showing':
                for book in books:
                    print(
                        f"\n{6*' '}{book} : ({', '.join(self.register[book]['lender'])})")
            elif type == 'returning':
                print(f"{', '.join(books)}")
                return books
        else:
            if type == 'returning':
                print('\nNo books to Return!')
                return []

    def donate(self):
        books = self.askTo('donate')
        if not books == ['']:
            self.register = self.addBook(self.register, books)
            self.wish('donate', 'books')
            print('Very very Thank you! To Donate books')
        return ['']

    def lend(self):
        self.allBooks()
        books = self.askTo('lend')
        if not books == ['']:
            for book in books:
                if book in self.books:
                    if self.availablity(book) > 0:
                        print(f'\nThe book {book} 📚 is available.')
                        name = input('\nEnter Your name: ')
                        if not name == '':
                            enter = input(
                                'Press Enter to lend books: \n').strip()
                            if enter == '':
                                self.register[book]['copy'] -= 1
                                self.register[book]['lender'].append(name)
                                self.wish('lend', 'books')
                        elif name == '':
                            print('\nYour name is not Entered!')
                    else:
                        print(
                            f"\nThe book 📚 '{book}' is already being used by {self.register[book]['lender']}")
                else:
                    print(f"\nThe book 📚 '{book}' is not available!")
        return ['']

    def returnBooks(self):
        unreturned = self.print_unreturned('returning')
        if not unreturned == []:
            lenders = ', '.join(self.lenders)
            print(f"The lenders are:\n{3*' '}{lenders}\n")
            name = input('Enter Your name: ')
            if not name == '':
                books = self.askTo('return')
                if not books == ['']:
                    enter = input('Press Enter to return books:\n')
                    if enter == '':
                        for book in books:
                            self.register[book]['copy'] += 1
                            self.register[book]['lender'].remove(name)
                        self.wish('returned', 'books')

    def run(self):
        print(f'Welcome to {self.name}:')

        while True:
            print('\nUse Following options:')
            action = input(
                "1. Available Books \n \
                 2. Lend Books \n \
                 3. Donate Books \n \
                 4. Return Books \n \
                 \n:⏩ "
            )

            if any([action == str(i) for i in range(1, 5)]):
                if action == '1':
                    self.allBooks()
                elif action == '2':
                    self.lend()
                elif action == '3':
                    self.donate()
                elif action == '4':
                    self.returnBooks()

            else:
                print('Please choose a valid option!')

            self.saveRegister()

            user_choice = input("\nPress Q to QUIT: ").lower()
            if user_choice == 'q':
                break


if __name__ == '__main__':
    Rahul = Library.set_properties(
        'Rahul-Library',
        ['C++', 'Python', 'Java']
    )
    Rahul.run()

    print('\n[programme finished]\n')
