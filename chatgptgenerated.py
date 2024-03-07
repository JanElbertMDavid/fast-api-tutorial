from fastapi import FastAPI, Path, Query, HTTPException
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello world!"}

@app.get("/blog/all")
async def get_all_blog(page: int = 1, page_size: Optional[int] = Query(None, ge=1, le=100)):
    return {"message": f"All {page_size} blogs on page {page}."}

@app.get("/blog/{id}/comments/{comment_id}")
async def get_comment(
    id: int = Path(..., title="The ID of the blog"),
    comment_id: int = Path(..., title="The ID of the comment"),
    valid: bool = Query(True, description="Whether the comment is valid or not"),
    username: Optional[str] = Query(None, title="The username of the commenter")):
    return {
        "message": f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}."
    }

class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"

@app.get("/blog/type/{type}")
async def get_blog_type(type: BlogType):
    return {"message": f"Blog type: {type.value}"}

@app.get("/blog/{id}")
async def get_blog(id: int, response: dict = None):
    if response is None:
        response = {"message": f"Blog with ID {id}."}
    else:
        response["message"] = f"Blog with ID {id}."
    return response
