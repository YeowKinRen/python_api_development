from turtle import title
from fastapi import Body, FastAPI
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str = "default"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/post")
async def root(new_post: Post):
    print(new_post.title)
    return {"message": "Hello World"}

# uvicorn main:app --reload