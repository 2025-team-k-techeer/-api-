from datetime import datetime
from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


sqlite_fname = "posts.db"
sqlite_url = f"sqlite:///{sqlite_fname}"

engine = create_engine(sqlite_url)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class BlogPost(Base):
    __tablename__ = "blog_posts"
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column()


class BlogPostJSON(BaseModel):
    id: int
    title: str
    author: str
    content: str
    timestamp: datetime


class QueryParams(BaseModel):
    id: int
    limit: int
    offset: int
    title: str | None
    author: str | None
    content: str | None


def create_db_and_tables():
    Base.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()

    seed_data = [
        BlogPost(
            id=1,
            title="Getting Started with FastAPI",
            author="Alice Kim",
            content="FastAPI is a modern web framework for building APIs with Python.",
            timestamp=datetime(2024, 7, 1, 10, 15),
        ),
        BlogPost(
            id=2,
            title="Understanding Python Async",
            author="Bob Lee",
            content="Async and await keywords help write non-blocking code using coroutines.",
            timestamp=datetime(2024, 7, 3, 14, 30),
        ),
        BlogPost(
            id=3,
            title="Deploying FastAPI to Heroku",
            author="Carla Zhang",
            content="Step-by-step guide to deploy your FastAPI app using Gunicorn and Heroku.",
            timestamp=datetime(2024, 7, 5, 9, 0),
        ),
        BlogPost(
            id=4,
            title="10 VSCode Extensions for Python Developers",
            author="David Cho",
            content="From Pylance to Jupyter, here are the top tools for productivity.",
            timestamp=datetime(2024, 7, 6, 16, 45),
        ),
        BlogPost(
            id=5,
            title="Building a Blog API",
            author="Emily Park",
            content="Learn how to create a simple REST API for managing blog posts using FastAPI.",
            timestamp=datetime(2024, 7, 8, 11, 20),
        ),
    ]

    with Session(engine) as session:
        if not session.query(BlogPost).first():  # Avoid duplicate seeding
            session.add_all(seed_data)
            session.commit()

    yield

    # No cleanup needed


def get_session():
    with Session(engine) as session:
        yield session
