from datetime import date
from typing import Any
from sqlalchemy import or_
from database.session import DatabaseManager
from models.employee import Employee
from utils.logger import get_logger
from utils.error_handler import handle_errors, DuplicateError, NotFoundError

logger = get_logger("services.employee")

class EmployeeService:
    @staticmethod
    @handle_errors(reraise=True)
    def create_employee(data: dict[str, Any]) -> Employee:
        session = DatabaseManager.get_session()
        try:
            existing = session.query(Employee).filter(
                or_(Employee.employee_code == data["employee_code"], Employee.email == data["email"])
            ).first()
            if existing:
                raise DuplicateError("Employee with this code or email already exists.")

            hire_date = data.get("hire_date")
            if isinstance(hire_date, str) and hire_date:
                hire_date = date.fromisoformat(hire_date)

            emp = Employee(
                employee_code=data["employee_code"].strip(),
                first_name=data["first_name"].strip(),
                last_name=data["last_name"].strip(),
                email=data["email"].strip().lower(),
                phone=data.get("phone", "").strip() or None,
                department=data["department"].strip(),
                position=data.get("position", "").strip() or None,
                salary=float(data.get("salary", 0.0) or 0.0),
                hire_date=hire_date,
                is_active=data.get("is_active", True)
            )
            session.add(emp)
            session.commit()
            session.refresh(emp)
            return emp
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def get_all(search: str | None = None, department: str | None = None, active_only: bool = False) -> list[Employee]:
        session = DatabaseManager.get_session()
        try:
            query = session.query(Employee)
            if search:
                search_term = f"%{search.strip()}%"
                query = query.filter(or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.email.ilike(search_term),
                    Employee.employee_code.ilike(search_term)
                ))
            if department and department != "All Departments":
                query = query.filter(Employee.department == department)
            if active_only:
                query = query.filter(Employee.is_active == True)
            return query.order_by(Employee.first_name, Employee.last_name).all()
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def get_by_id(employee_id: int) -> Employee | None:
        session = DatabaseManager.get_session()
        try:
            return session.query(Employee).filter(Employee.id == employee_id).first()
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def update_employee(employee_id: int, data: dict[str, Any]) -> Employee:
        session = DatabaseManager.get_session()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if not emp:
                raise NotFoundError(f"Employee with ID {employee_id} not found.")

            existing = session.query(Employee).filter(
                or_(Employee.employee_code == data["employee_code"], Employee.email == data["email"]),
                Employee.id != employee_id
            ).first()
            if existing:
                raise DuplicateError("Another employee with this code or email already exists.")

            emp.employee_code = data["employee_code"].strip()
            emp.first_name = data["first_name"].strip()
            emp.last_name = data["last_name"].strip()
            emp.email = data["email"].strip().lower()
            emp.phone = data.get("phone", "").strip() or None
            emp.department = data["department"].strip()
            emp.position = data.get("position", "").strip() or None
            emp.salary = float(data.get("salary", 0.0) or 0.0)
            emp.is_active = data.get("is_active", True)

            hire_date = data.get("hire_date")
            if isinstance(hire_date, str) and hire_date:
                emp.hire_date = date.fromisoformat(hire_date)
            elif isinstance(hire_date, date):
                emp.hire_date = hire_date

            session.commit()
            session.refresh(emp)
            return emp
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def delete_employee(employee_id: int) -> bool:
        session = DatabaseManager.get_session()
        try:
            emp = session.query(Employee).filter(Employee.id == employee_id).first()
            if not emp:
                raise NotFoundError(f"Employee with ID {employee_id} not found.")
            session.delete(emp)
            session.commit()
            return True
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    @handle_errors(reraise=True)
    def get_departments() -> list[str]:
        session = DatabaseManager.get_session()
        try:
            results = session.query(Employee.department).distinct().all()
            return sorted([r[0] for r in results if r[0]])
        finally:
            session.close()