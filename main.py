from fastapi import FastAPI, Response, status
from enum import Enum
from typing import Optional
from routers import blog_get
from routers import blog_post

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get("/")
# Returns a hello world message.
def HelloWorld():
    return {"message": "Hello world!"}
