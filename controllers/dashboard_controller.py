from typing import Any
from services.dashboard_service import DashboardService
from utils.logger import get_logger

logger = get_logger("controllers.dashboard")

class DashboardController:
    @staticmethod
    def get_dashboard_data() -> dict[str, Any]:
        return {
            "total_employees": DashboardService.get_total_employees(),
            "active_employees": DashboardService.get_active_employees(),
            "department_count": DashboardService.get_department_count(),
            "today_attendance": DashboardService.get_today_attendance(),
            "department_distribution": DashboardService.get_department_distribution(),
            "attendance_trend": DashboardService.get_attendance_trend(30)
        }