import Library as lib
from typing import NoReturn


class Library(lib.Library):

    def __init__(self, library_name: str, initial_books: list, register: dict) -> None:
        super().__init__(library_name, initial_books, register)

    ################### Extra Methods ###################

    def run(self) -> NoReturn:

        while True:
            print(self.welcomeMsg)
            action = int(input("Enter a choice:⏩ "))

            if action == 1:
                self.displayAvailableBooks()
            elif action == 2:
                self.borrowBooks(self.customer.askTo('borrow'))
            elif action == 3:
                self.returnBooks(self.customer.askTo('donate'))
            elif action == 4:
                self.returnBooks(self.customer.askTo('return'))
            elif action == 5:
                print(
                    f"Thanks for choosing {self.name}. Have a great day ahead!")
                break
            else:
                print("Invalid Choice!")


if __name__ == "__main__":
    centralLibrary = Library.set_properties(
        'Central Library',
        ['Python', 'Java']
    )

    centralLibrary.run()
