from fastapi import HTTPException
from db.models import DbArticle
from sqlalchemy.orm.session import Session
from exceptions import StoryException
from schemas import ArticleBase

def create_article(db: Session, request: ArticleBase):
    if request.content.startswith('Once upon a time'):
        raise StoryException('No stories please!')
    new_article = DbArticle(
        title = request.title,
        content = request.content,
        published = request.published,
        user_id = request.creator_id
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_article(db: Session, id: int):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    # Handle errors
    if not article:
        raise HTTPException(status_code=404, detail=f'Article with ID: {id} not found.')
    return article