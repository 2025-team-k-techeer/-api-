from fastapi import FastAPI, HTTPException, Query, Body, Depends
from typing import Annotated, List
from models import (
    datetime,
    BlogPost,
    BlogPostJSON,
    QueryParams,
    get_session,
    lifespan,
    Session,
)

app = FastAPI(lifespan=lifespan)


@app.get("/posts", response_model=List[BlogPostJSON])
def postings(db: Session = Depends(get_session)):
    return db.query(BlogPost).all()


@app.get("/posts/{post_id}", response_model=BlogPostJSON)
def get_post(post_id: int, db: Session = Depends(get_session)):
    post = db.get(BlogPost, post_id)
    if post is None:
        return {"error": "Post not found"}
    return post


@app.delete("/posts/{post_id}", response_model=BlogPostJSON)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    deleted = db.get(BlogPost, post_id)
    if deleted is None:
        return {"error": "Post not found"}
    db.delete(deleted)
    db.commit()
    return deleted


@app.post("/posts/", response_model=BlogPostJSON)
def add_post(
    new_post: Annotated[BlogPostJSON, Body()], db: Session = Depends(get_session)
):
    new_row = BlogPost(
        author=new_post.author,
        title=new_post.title,
        content=new_post.content,
        timestamp=new_post.timestamp,
    )
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


@app.put("/posts/{post_id}", response_model=BlogPostJSON)
def edit_post(
    post_id: int,
    edit: Annotated[BlogPostJSON, Body()],
    db: Session = Depends(get_session),
):
    post = db.get(BlogPost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = edit.title
    post.content = edit.content
    post.author = edit.author
    post.timestamp = edit.timestamp

    db.commit()
    db.refresh(post)
    return post


@app.get("/")
def home():
    return {"message": "Hello World"}
