from controllers.employee_controller import EmployeeController
from controllers.attendance_controller import AttendanceController
from utils.pdf_exporter import PDFExporter
from utils.excel_exporter import ExcelExporter
from utils.logger import get_logger

logger = get_logger("controllers.reports")

class ReportsController:
    @staticmethod
    def generate_employee_pdf(file_path: str) -> bool:
        data = EmployeeController.get_employees()
        return PDFExporter.export_employees(file_path, data)

    @staticmethod
    def generate_employee_excel(file_path: str) -> bool:
        data = EmployeeController.get_employees()
        return ExcelExporter.export_employees(file_path, data)

    @staticmethod
    def generate_attendance_pdf(file_path: str) -> bool:
        data = AttendanceController.get_history(days=30)
        return PDFExporter.export_attendance(file_path, data)