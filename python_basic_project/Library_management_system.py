class Book:
    Book_list = ["Math","Science","Physics","Chemistry"]
    def __init__(self,Name):
        self.name = Name
        if self.name == self.Book_list:
            print(f"{self.name} Book is available")
        else:
            print("Not available")

class librarian(Book):
    def addbook(self,bookname):
        self.bookname = bookname
        if self.bookname != self.Book_list:
            self.Book_list+= self.addbook

    def removebook(self,book):
        self.removebook = book
        if self.removebook == self.Book_list:
            self.Book_list -= self.removebook

    def lendbook(self,book,username):
        self.book = book
        self.username = username
        if self.lendbook == self.Book_list:
            self.lendbook += self.username
            print(f"{self.username} takes {self.lendbook} from the library")

    def borrowbook(self):
        if self.username == self.lendbook:
            print(f"{self.username} borrowed {self.lendbook} from the library")



class User(librarian):
    def __init__(self, Username):
        self.username = Username
        print(f"{Username} has borrowed {self.lendbook} from the library")

import math
a = Book(math)
print(a.Book_list)




#code 1

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"{'[Available]' if self.is_available else '[Borrowed]'} {self.title} by {self.author}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book_title):
        for book in library.books:
            if book.title == book_title and book.is_available:
                book.is_available = False
                self.borrowed_books.append(book)
                print(f"{self.name} borrowed '{book.title}'.")
                break
            else:
                print(f"Sorry, '{book_title}' is already borrowed.")


    def return_book(self, book_title):
        for book in library.books:
            if book in self.borrowed_books and book.title.is_available:
                self.borrowed_books.remove(book)
                print(f"{self.name} returned '{book.title}'.")
            else:
                print(f"{self.name} does not have '{book.title}'.")

    def view_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name}'s Borrowed Books:")
            for book in self.borrowed_books:
                print(f"- {book.title} by {book.author}")
        else:
            print(f"{self.name} has not borrowed any books.")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        print(f"Book '{title}' by {author} added to the library.")

    def remove_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                print(f"Book '{title}' removed from the library.")
                return
        print(f"Book '{title}' not found in the library.")

    def list_books(self):
        if self.books:
            print("Library Books:")
            for book in self.books:
                print(f"- {book}")
        else:
            print("The library has no books.")

library = Library()
library.add_book("Python", "Henry")
library.add_book("ML", "org")
library.list_books()
user = User("Heril")
user.borrow_book('Python')
user.view_borrowed_books()
user.return_book("ML")
# Example Usage
if __name__ == "__main__":
    library = Library()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    library.add_book("1984", "George Orwell")
    library.list_books()
    
    user1 = User("Alice")
    user1.borrow_book(library.books[0])  # Borrow "The Great Gatsby"
    user1.view_borrowed_books()
    
    user1.return_book(library.books[0])  # Return "The Great Gatsby"
    user1.view_borrowed_books()
    
    library.list_books()



#code 2

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"{'[Available]' if self.is_available else '[Borrowed]'} {self.title} by {self.author}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available:
            book.is_available = False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed '{book.title}'.")
        else:
            print(f"Sorry, '{book.title}' is already borrowed.")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.is_available = True
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'.")
        else:
            print(f"{self.name} does not have '{book.title}'.")

    def view_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name}'s Borrowed Books:")
            for book in self.borrowed_books:
                print(f"- {book.title} by {book.author}")
        else:
            print(f"{self.name} has not borrowed any books.")


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)
        print(f"Book '{title}' by {author} added to the library.")

    def remove_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                print(f"Book '{title}' removed from the library.")
                return
        print(f"Book '{title}' not found in the library.")

    def list_books(self):
        if self.books:
            print("Library Books:")
            for book in self.books:
                print(f"- {book}")
        else:
            print("The library has no books.")


def main():
    library = Library()
    users = {}
    
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. List Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Borrowed Books")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            library.add_book(title, author)
        elif choice == "2":
            title = input("Enter book title to remove: ")
            library.remove_book(title)
        elif choice == "3":
            library.list_books()
        elif choice == "4":
            user_name = input("Enter your name: ")
            if user_name not in users:
                users[user_name] = User(user_name)
            title = input("Enter book title to borrow: ")
            for book in library.books:
                if book.title == title:
                    users[user_name].borrow_book(book)
                    break
            else:
                print("Book not found.")
        elif choice == "5":
            user_name = input("Enter your name: ")
            if user_name in users:
                title = input("Enter book title to return: ")
                for book in users[user_name].borrowed_books:
                    if book.title == title:
                        users[user_name].return_book(book)
                        break
                else:
                    print("You don't have this book.")
            else:
                print("User not found.")
        elif choice == "6":
            user_name = input("Enter your name: ")
            if user_name in users:
                users[user_name].view_borrowed_books()
            else:
                print("User not found.")
        elif choice == "7":
            print("Exiting Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

# Example Run:
# Enter your choice: 1
# Enter book title: The Hobbit
# Enter book author: J.R.R. Tolkien
# Book 'The Hobbit' by J.R.R. Tolkien added to the library.
# Enter your choice: 3
# Library Books:
# - [Available] The Hobbit by J.R.R. Tolkien
# Enter your choice: 4
# Enter your name: Alice
# Enter book title to borrow: The Hobbit
# Alice borrowed 'The Hobbit'.
# Enter your choice: 6
# Enter your name: Alice
# Alice's Borrowed Books:
# - The Hobbit by J.R.R. Tolkien


import math

print(math.add(1,2))
