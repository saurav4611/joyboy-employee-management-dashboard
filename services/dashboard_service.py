from datetime import date, timedelta
from sqlalchemy import func, distinct
from database.session import DatabaseManager
from models.employee import Employee
from models.attendance import Attendance
from utils.logger import get_logger
from utils.error_handler import handle_errors

logger = get_logger("services.dashboard")

class DashboardService:
    @staticmethod
    @handle_errors(reraise=False, default=0)
    def get_total_employees() -> int:
        session = DatabaseManager.get_session()
        try:
            return session.query(func.count(Employee.id)).scalar() or 0
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=False, default=0)
    def get_active_employees() -> int:
        session = DatabaseManager.get_session()
        try:
            return session.query(func.count(Employee.id)).filter(Employee.is_active == True).scalar() or 0
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=False, default=0)
    def get_department_count() -> int:
        session = DatabaseManager.get_session()
        try:
            return session.query(func.count(distinct(Employee.department))).scalar() or 0
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=False, default=0)
    def get_today_attendance() -> int:
        session = DatabaseManager.get_session()
        try:
            today = date.today()
            return session.query(func.count(Attendance.id)).filter(
                Attendance.date == today,
                Attendance.status == "present"
            ).scalar() or 0
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=False, default=[])
    def get_department_distribution() -> list[tuple[str, int]]:
        session = DatabaseManager.get_session()
        try:
            results = session.query(
                Employee.department,
                func.count(Employee.id)
            ).group_by(Employee.department).order_by(func.count(Employee.id).desc()).all()
            return [(dept, count) for dept, count in results]
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=False, default=[])
    def get_attendance_trend(days: int = 30) -> list[tuple[str, int]]:
        session = DatabaseManager.get_session()
        try:
            today = date.today()
            start_date = today - timedelta(days=days)
            
            results = session.query(
                Attendance.date,
                func.count(Attendance.id)
            ).filter(
                Attendance.date >= start_date,
                Attendance.date <= today,
                Attendance.status == "present"
            ).group_by(Attendance.date).order_by(Attendance.date).all()
            
            date_count_map = {d: c for d, c in results}
            trend = []
            current = start_date
            while current <= today:
                count = date_count_map.get(current, 0)
                trend.append((current.strftime("%m-%d"), count))
                current += timedelta(days=1)
            return trend
        finally:
            session.close()