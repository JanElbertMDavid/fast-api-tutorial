from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_article
from auth.oauth2 import get_current_user, oauth2_scheme

from schemas import ArticleBase, ArticleDisplay, UserBase

router = APIRouter(
    prefix='/article',
    tags=['article']
)

# Create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)

# Get specific article
@router.get('/{id}')#, response_model=ArticleDisplay)
def get_article_by_id(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data':db_article.get_article(db, id),
        'current_user': current_user
    }