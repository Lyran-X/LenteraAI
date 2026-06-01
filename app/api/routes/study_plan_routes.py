import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth_schema import MessageResponse
from app.schemas.study_plan_schema import StudyPlanGenerateRequest, StudyPlanItemUpdateRequest, StudyPlanRead
from app.services.study_plan_service import study_plan_service


router = APIRouter(prefix="/study-plans", tags=["Study Plans"])


@router.get("/context")
def get_study_plan_context(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    return {
        "feature": "study-plans",
        "user_id": str(current_user.id),
        "role": current_user.role,
        "message": "Study Plan endpoints scope all data to current_user.id.",
    }


@router.post("/generate", response_model=StudyPlanRead, status_code=status.HTTP_201_CREATED)
def generate_study_plan(
    payload: StudyPlanGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.generate_study_plan(db=db, current_user=current_user, payload=payload)


@router.get("", response_model=list[StudyPlanRead])
def get_study_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[StudyPlanRead]:
    return study_plan_service.get_study_plans(db=db, current_user=current_user)


@router.get("/active", response_model=StudyPlanRead)
def get_active_study_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.get_active_study_plan(db=db, current_user=current_user)


@router.get("/{plan_id}", response_model=StudyPlanRead)
def get_study_plan(
    plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.get_study_plan(db=db, current_user=current_user, plan_id=plan_id)


@router.patch("/items/{item_id}", response_model=StudyPlanRead)
def update_item(
    item_id: uuid.UUID,
    payload: StudyPlanItemUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.update_study_plan_item(
        db=db,
        current_user=current_user,
        item_id=item_id,
        payload=payload,
    )


@router.delete("/items/{item_id}", response_model=StudyPlanRead)
def delete_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.delete_study_plan_item(db=db, current_user=current_user, item_id=item_id)


@router.patch("/items/{item_id}/complete", response_model=StudyPlanRead)
def complete_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.complete_item(db=db, current_user=current_user, item_id=item_id)


@router.patch("/items/{item_id}/uncomplete", response_model=StudyPlanRead)
def uncomplete_item(
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> StudyPlanRead:
    return study_plan_service.uncomplete_item(db=db, current_user=current_user, item_id=item_id)


@router.delete("/{plan_id}", response_model=MessageResponse)
def delete_study_plan(
    plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> MessageResponse:
    study_plan_service.delete_study_plan(db=db, current_user=current_user, plan_id=plan_id)
    return MessageResponse(message="Study plan deleted.")

