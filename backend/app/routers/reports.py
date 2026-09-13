from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.report import ReportCreate, ReportResponse
from app.services.report_service import (
    create_report,
    get_all_reports,
    get_report_by_id,
    close_report,
    get_user_report
)
from app.services.review_service import get_review_by_id
from app.core.auth import get_current_customer, get_current_admin


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/review/{review_id}", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def report_review(
    review_id: int,
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_customer)
):
    review = get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    if review.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot report your own review"
        )

    existing_report = get_user_report(
        db,
        review_id,
        current_user.id
    )

    if existing_report:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reported this review"
        )

    return create_report(
        db,
        review_id,
        current_user.id,
        report_data.reason
    )


@router.get("", response_model=List[ReportResponse])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return get_all_reports(db)


@router.put("/{report_id}/close", response_model=ReportResponse)
def close_existing_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    report = get_report_by_id(db, report_id)

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return close_report(db, report)