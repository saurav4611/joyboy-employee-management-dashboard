from datetime import date, timedelta
from typing import Any
from services.attendance_service import AttendanceService
from utils.logger import get_logger

logger = get_logger("controllers.attendance")

class AttendanceController:
    @staticmethod
    def mark_attendance(employee_id: int, att_date: date, status: str, notes: str = "") -> dict[str, Any] | None:
        record = AttendanceService.mark_attendance(employee_id, att_date, status, notes)
        return record.to_dict() if record else None

    @staticmethod
    def get_history(days: int = 30) -> list[dict[str, Any]]:
        start_date = date.today() - timedelta(days=days)
        records = AttendanceService.get_history(start_date=start_date, end_date=date.today())
        return [r.to_dict() for r in records]

    @staticmethod
    def get_monthly_summary(year: int, month: int) -> list[dict[str, Any]]:
        return AttendanceService.get_monthly_summary(year, month)