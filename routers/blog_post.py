from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(prefix="/blog", tags=["blog"])


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    nb_comments: int
    tags: List[str] = []
    metadata: Dict[str, str] = {'Key1': 'Val1'}
    image: Optional[Image] = None


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"id": id, "data": blog, "version": version}


@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: int = Query(
        None,
        title="The title of the comment",
        description="Some description for comment title.",
        alias="commentTitle",
        deprecated=True,
    ),
    content: str = Body(..., min_length=10, max_length=12, regex="^[a-z\s]*$"),
    v: List[Optional[str]] = Query(['1.0','2.0','4.0']),
    comment_id: int = Path(..., gt=5, le=10)
):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
    }

def required_functionality():
    return {'message': 'Learning fastAPI is important.'}
