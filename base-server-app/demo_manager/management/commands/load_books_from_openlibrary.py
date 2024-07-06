import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from ...models import Author, Book, BookWithIndex

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file_dir",
                            type=str,
                            help="file directory of openlibrary search response json format e.g. "
                                 "'https://openlibrary.org/search.json?q=a&limit=1000'")
        parser.add_argument("--withindex", action="store_true", help="Load with model BookWithIndex")
        parser.add_argument("--ignore_duplicate", action="store_true", help="Ignore duplicate book")

    @staticmethod
    def load_json_file(kwargs):
        file_dir = kwargs.get("file_dir")
        if not file_dir:
            raise CommandError("file_dir is required")

        try:
            with open(file_dir, "r") as f:
                book_search_json = json.load(f)
        except FileNotFoundError:
            raise CommandError("file_dir not found")

        return book_search_json

    def handle(self, *args, **kwargs):
        is_model_bookwithindex = kwargs['withindex']
        is_ignore_duplicate = kwargs['ignore_duplicate']
        book_search_json = self.load_json_file(kwargs)
        book_results = book_search_json["docs"]
        imported_books = 0
        book_class = BookWithIndex if is_model_bookwithindex else Book

        for book in book_results:
            isbn_list = book.get("isbn")
            isbn = isbn_list[0] if isbn_list else ""
            existing_books = book_class.objects.filter(title=book["title"], isbn=isbn).count()

            if not is_ignore_duplicate and existing_books > 0:
                continue

            authors = []
            for author_name in book.get("author_name", []):
                author, _created = Author.objects.get_or_create(name=author_name)
                authors.append(author.id)

            if not authors:
                continue

            if existing_books > 0:
                book_obj = book_class.objects.create(title=f'{book["title"]}_{existing_books}', isbn=isbn)
            else:
                book_obj = book_class.objects.create(title=book["title"], isbn=isbn)

            book_obj.authors.add(*authors)
            imported_books += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import {imported_books} books successfully"
        ))
