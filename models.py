class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

    def print_author(self) -> None:
        print(self.author)


book = Book('Book', 'Manolo')
book.print_author()
