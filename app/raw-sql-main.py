from random import randrange
from typing import Optional

import psycopg2
from fastapi import Body, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="password",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was successfull")
except Exception as error:
    print("Database connection was unsuccessfull")
    print("Error: ", error)

my_posts = [
    {
        "title": "This is a api",
        "content": "Api is used for data",
        "published": False,
        "rating": 4,
        "id": 1,
    },
    {
        "title": "This is a api 1",
        "content": "Api is used for data 2",
        "published": True,
        "rating": 7,
        "id": 2,
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World !"}


@app.get("/posts")
async def post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    curr_post = cursor.fetchone()
    conn.commit()
    return {"data": curr_post}


def find_post(id):
    for p in my_posts:
        if p["id"] == int(id):
            return p


def find_post_idx(id):
    for i, p in enumerate(my_posts):
        if p["id"] == int(id):
            return i


@app.get("/post/{id}")
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id)))
    curr_post = cursor.fetchone()
    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"post_details": curr_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
        (post.title, post.content, post.published, str(id)),
    )
    conn.commit()
    update_post = cursor.fetchone()
    if update_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"data": update_post}
