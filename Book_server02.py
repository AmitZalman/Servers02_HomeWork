from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi import Response, status

import Book_dal
Book_dal.create_table_books()

# pip install uvicorn fastapi
# uvicorn 01_servers:app --port 8002 --reload
# swagger: http://127.0.0.1:8002/docs

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    language: str
    price: float
    published_year: int



class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    language: Optional[str] = None
    price: Optional[float] = None
    published_year: Optional[int] = None



@app.get("/", response_class=HTMLResponse)
def basic_url():
    return "Welcome!"


# ---- GET all ----
@app.get("/books")
def get_books():
    return Book_dal.get_all_books()


# ---- GET by id ----
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int, response: Response):
    book = Book_dal.get_book_by_id(book_id)
    if not book:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {}
    return book


# ---- POST create ----
@app.post("/books")
def create_book(book: Book, response: Response):
    row_id = Book_dal.insert_book(book.title, book.author, book.language, book.price ,book.published_year)
    new_book = {**book.__dict__, "id": row_id}
    response.status_code = status.HTTP_201_CREATED
    return {"message": "book created", "book": new_book,
            "url": f"/books/{row_id}"}


# ---- PUT full update ----
# Replaces the entire product; if not found, creates a new one
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book, response: Response):
    updated = Book_dal.update_book(book_id ,book.title, book.author, book.language, book.price ,book.published_year)
    if updated:
        return {"message": "book updated", "item": {**book.__dict__, "id": book_id}}

    # Not found → create new
    row_id = Book_dal.insert_book(book.title, book.author, book.language, book.price ,book.published_year)
    new_book = {**book.__dict__, "id": row_id}
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Book created", "book": new_book,
            "url": f"/books/{row_id}"}

# ---- DELETE by id ----
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = Book_dal.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"book id={book_id} not found")
    return {"message": f"Book {book_id} deleted"}


# ---- DROP & recreate products table ----
@app.delete("/tables/books")
def drop_table_books():
    Book_dal.drop_table_books()
    return {"message": "Table dropped and recreated"}
