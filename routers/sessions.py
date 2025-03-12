from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as SQLSession, select
from models import Session
from schemas import SessionCreate, SessionUpdate, SessionResponse
from database import get_session
from datetime import datetime

router = APIRouter(tags=["Sessions"])

@router.get("/sessions", response_model=List[SessionResponse])
def get_sessions(
    status: Optional[str] = None,
    db: SQLSession = Depends(get_session)
):
    query = select(Session)
    if status:
        query = query.where(Session.status == status)
    sessions = db.exec(query).all()
    return sessions

@router.get("/sessions/{id}", response_model=SessionResponse)
def get_session(id: int, db: SQLSession = Depends(get_session)):
    session = db.get(Session, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/sessions", response_model=SessionResponse)
def create_session(
    session_create: SessionCreate,
    db: SQLSession = Depends(get_session)
):
    new_session = Session.from_orm(session_create)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.put("/sessions/{id}", response_model=SessionResponse)
def update_session(
    id: int,
    session_update: SessionUpdate,
    db: SQLSession = Depends(get_session)
):
    session = db.get(Session, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    update_data = session_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(session, key, value)

    if session.end_time and not session.duration_minutes:
        session.duration_minutes = int(
            (session.end_time - session.start_time).total_seconds() // 60
        )
        session.status = "completed"

    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.put("/sessions/{id}/end", response_model=SessionResponse)
def end_session(id: int, db: SQLSession = Depends(get_session)):
    session = db.get(Session, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.end_time = datetime.utcnow()
    session.duration_minutes = int(
        (session.end_time - session.start_time).total_seconds() // 60
    )
    session.status = "completed"

    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.delete("/sessions/{id}")
def delete_session(id: int, db: SQLSession = Depends(get_session)):
    session = db.get(Session, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}
