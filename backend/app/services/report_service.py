from sqlalchemy.orm import Session

from app.models.report import Report


def create_report(db: Session, review_id: int, user_id: int, reason: str):
    report = Report(
        review_id=review_id,
        user_id=user_id,
        reason=reason,
        status="pending"
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_all_reports(db: Session):
    return db.query(Report).all()


def get_report_by_id(db: Session, report_id: int):
    return (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )


def close_report(db: Session, report: Report):
    report.status = "closed"

    db.commit()
    db.refresh(report)

    return report

def get_user_report(db: Session, review_id: int, user_id: int):
    return (
        db.query(Report)
        .filter(
            Report.review_id == review_id,
            Report.user_id == user_id
        )
        .first()
    )