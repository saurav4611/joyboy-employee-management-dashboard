from typing import Any
from services.employee_service import EmployeeService
from utils.logger import get_logger

logger = get_logger("controllers.employee")

class EmployeeController:
    @staticmethod
    def get_employees(search: str | None = None, department: str | None = None, active_only: bool = False) -> list[dict[str, Any]]:
        employees = EmployeeService.get_all(search=search, department=department, active_only=active_only)
        return [emp.to_dict() for emp in employees]

    @staticmethod
    def get_departments() -> list[str]:
        return EmployeeService.get_departments()

    @staticmethod
    def create_employee(data: dict[str, Any]) -> dict[str, Any]:
        emp = EmployeeService.create_employee(data)
        return emp.to_dict()

    @staticmethod
    def update_employee(employee_id: int, data: dict[str, Any]) -> dict[str, Any]:
        emp = EmployeeService.update_employee(employee_id, data)
        return emp.to_dict()

    @staticmethod
    def delete_employee(employee_id: int) -> bool:
        return EmployeeService.delete_employee(employee_id)