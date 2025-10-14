from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import paint as paint_schema
from app.crud import crud_paint
from app.api.v1 import deps

router = APIRouter()


@router.post(
    "/", response_model=paint_schema.Paint, status_code=status.HTTP_201_CREATED
)
def create_paint(
    *, db: Session = Depends(deps.get_db), paint_in: paint_schema.PaintCreate
):
    """
    Create a new paint.
    (This endpoint should be protected in a real app)
    """
    paint = crud_paint.create_paint(db=db, paint=paint_in)
    return paint


@router.get("/", response_model=list[paint_schema.Paint])
def read_paints(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100):
    """
    Retrieve paints.
    """
    paints = crud_paint.get_paints(db, skip=skip, limit=limit)
    return paints
