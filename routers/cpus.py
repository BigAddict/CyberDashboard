from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import CPU
from schemas import CPUCreate, CPUUpdate, CPUResponse
from database import get_session
import uuid

router = APIRouter(prefix="/cpus", tags=["CPUs"])

@router.get("/", response_model=list[CPUResponse])
async def get_cpus(session: Session = Depends(get_session)):
    cpus = session.exec(select(CPU)).all()
    return cpus

@router.get("/{cpu_id}", response_model=CPUResponse)
async def get_cpu(cpu_id: str, session: Session = Depends(get_session)):
    cpu = session.get(CPU, cpu_id)
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU not found")
    return cpu

@router.post("/", response_model=CPUResponse)
async def register_cpu(cpu_data: CPUCreate, session: Session = Depends(get_session)):
    cpu_id = str(uuid.uuid4())
    new_cpu = CPU(id=cpu_id, **cpu_data.dict())
    session.add(new_cpu)
    session.commit()
    session.refresh(new_cpu)
    return new_cpu

@router.put("/{cpu_id}", response_model=CPUResponse)
async def update_cpu(cpu_id: str, cpu_data: CPUUpdate, session: Session = Depends(get_session)):
    cpu = session.get(CPU, cpu_id)
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU not found")
    for key, value in cpu_data.dict(exclude_unset=True).items():
        setattr(cpu, key, value)
    session.add(cpu)
    session.commit()
    session.refresh(cpu)
    return cpu

@router.delete("/{cpu_id}")
async def delete_cpu(cpu_id: str, session: Session = Depends(get_session)):
    cpu = session.get(CPU, cpu_id)
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU not found")
    session.delete(cpu)
    session.commit()
    return {"message": "CPU deleted successfully"}