from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db
from dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.SchemeResponse])
def get_schemes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schemes = db.query(models.Scheme).offset(skip).limit(limit).all()
    return schemes

@router.get("/{scheme_id}", response_model=schemas.SchemeResponse)
def get_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.post("/save")
def save_scheme(scheme_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
        
    saved = db.query(models.SavedScheme).filter(
        models.SavedScheme.user_id == current_user.id,
        models.SavedScheme.scheme_id == scheme_id
    ).first()
    
    if saved:
        return {"message": "Scheme already saved"}
        
    new_saved = models.SavedScheme(user_id=current_user.id, scheme_id=scheme_id)
    db.add(new_saved)
    db.commit()
    return {"message": "Scheme saved successfully"}

@router.get("/saved/me")
def get_saved_schemes(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = db.query(models.SavedScheme).filter(models.SavedScheme.user_id == current_user.id).all()
    return [{"saved_id": s.id, "scheme": s.scheme} for s in saved]
