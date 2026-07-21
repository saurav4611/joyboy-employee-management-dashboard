from datetime import date, time, timedelta
from typing import Any
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from database.session import DatabaseManager
from models.employee import Employee
from models.attendance import Attendance
from utils.logger import get_logger
from utils.error_handler import handle_errors, NotFoundError

logger = get_logger("services.attendance")

class AttendanceService:
    @staticmethod
    @handle_errors(reraise=True)
    def mark_attendance(employee_id: int, att_date: date, status: str, notes: str = "") -> Attendance:
        session = DatabaseManager.get_session()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if not emp:
                raise NotFoundError(f"Employee with ID {employee_id} not found.")

            # joinedload use kiya hai taaki employee data pehle se load ho jaye
            existing = session.query(Attendance).options(joinedload(Attendance.employee)).filter(
                Attendance.employee_id == employee_id,
                Attendance.date == att_date
            ).first()

            if existing:
                existing.status = status
                existing.notes = notes
                if status == "present":
                    existing.check_in_time = time(9, 0)
                    existing.check_out_time = time(17, 0)
                else:
                    existing.check_in_time = None
                    existing.check_out_time = None
                session.commit()
                session.refresh(existing)
                # Session band hone se pehle employee object ko memory me load karne ke liye
                _ = existing.employee 
                return existing

            new_record = Attendance(
                employee_id=employee_id,
                date=att_date,
                status=status,
                check_in_time=time(9, 0) if status == "present" else None,
                check_out_time=time(17, 0) if status == "present" else None,
                notes=notes
            )
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            # Session band hone se pehle employee object ko memory me load karne ke liye
            _ = new_record.employee
            return new_record
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def mark_present(employee_id: int, att_date: date | None = None) -> Attendance:
        att_date = att_date or date.today()
        return AttendanceService.mark_attendance(employee_id, att_date, "present")

    @staticmethod
    @handle_errors(reraise=True)
    def mark_absent(employee_id: int, att_date: date | None = None) -> Attendance:
        att_date = att_date or date.today()
        return AttendanceService.mark_attendance(employee_id, att_date, "absent")

    @staticmethod
    @handle_errors(reraise=True)
    def get_history(employee_id: int | None = None, start_date: date | None = None, end_date: date | None = None, status: str | None = None) -> list[Attendance]:
        session = DatabaseManager.get_session()
        try:
            query = session.query(Attendance).options(joinedload(Attendance.employee))
            if employee_id:
                query = query.filter(Attendance.employee_id == employee_id)
            if start_date:
                query = query.filter(Attendance.date >= start_date)
            if end_date:
                query = query.filter(Attendance.date <= end_date)
            if status:
                query = query.filter(Attendance.status == status)
            return query.order_by(Attendance.date.desc(), Attendance.employee_id).all()
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def get_monthly_summary(year: int, month: int) -> list[dict[str, Any]]:
        session = DatabaseManager.get_session()
        try:
            first_day = date(year, month, 1)
            if month == 12:
                last_day = date(year, 12, 31)
            else:
                last_day = date(year, month + 1, 1) - timedelta(days=1)

            employees = session.query(Employee).filter(Employee.is_active == True).all()
            summaries = []

            for emp in employees:
                records = session.query(Attendance).filter(
                    and_(
                        Attendance.employee_id == emp.id,
                        Attendance.date >= first_day,
                        Attendance.date <= last_day
                    )
                ).all()

                present = sum(1 for r in records if r.status == "present")
                absent = sum(1 for r in records if r.status == "absent")
                total = len(records)
                rate = (present / total * 100) if total > 0 else 0.0

                summaries.append({
                    "employee_id": emp.id,
                    "employee_code": emp.employee_code,
                    "employee_name": emp.full_name,
                    "department": emp.department,
                    "present": present,
                    "absent": absent,
                    "total": total,
                    "rate": round(rate, 2)
                })
            return summaries
        finally:
            session.close()