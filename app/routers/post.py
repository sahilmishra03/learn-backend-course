from fastapi import HTTPException, Response, status, Depends,APIRouter
from app import oauth2
from .. import models, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=list[schemas.PostOut])
async def post(db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):  # cursor.execute(
    #     """INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # curr_post = cursor.fetchone()
    # conn.commit()
    
    # note: current_user is obtained via dependency but not currently stored on posts
    owner_id = current_user.id
    new_post = models.Post(owner_id=owner_id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id)))
    # curr_post = cursor.fetchone()
    curr_post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return curr_post


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_posts(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    if delete_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # conn.commit()
    # update_post = cursor.fetchone()

    update_post = db.query(models.Post).filter(models.Post.id == id)
    p = update_post.first()

    if p is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    if p.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    update_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_post.first()

