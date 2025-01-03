from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app1 = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithIris',
                'description': 'A new book',
                'rating': 5,
                'published_date': 2029,
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithiris', 'A very nice book!', 5, 2030),
    Book(2, 'Be fast with FastAPI', 'codingwithiris', 'A great nice book!', 5, 2030),
    Book(3, 'Master Endpoints', 'notwithstanding', 'A awesome book nice book!', 5, 2029),
    Book(4, 'Hp1', 'Author 1', 'A very nice book!', 2, 2028),
    Book(5, 'Hp 2', 'Author 2', 'A very nice book!', 3, 2027),
    Book(6, 'Hp 3', 'Author 3', 'A very nice book!', 5, 2026)
]


@app1.get("/books",status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app1.get("/books/",status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating: int= Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app1.get("/books/publish/",status_code=status.HTTP_200_OK)
async def get_books_published(publish_date: int=Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books_to_return.append(book)
    return books_to_return


@app1.post("/books/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app1.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app1.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    book_changed = False
    for i in range(0, len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail='Book not found')


@app1.delete("/books/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail='Book not found')

