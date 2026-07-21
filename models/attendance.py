from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship
from database.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="uq_employee_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="absent")
    check_in_time = Column(Time, nullable=True)
    check_out_time = Column(Time, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    employee = relationship("Employee", back_populates="attendance_records")

    @property
    def status_label(self) -> str:
        return self.status.title()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "employee_name": self.employee.full_name if self.employee else None,
            "employee_code": self.employee.employee_code if self.employee else None,
            "department": self.employee.department if self.employee else None,
            "date": self.date.isoformat() if self.date else None,
            "status": self.status,
            "status_label": self.status_label,
            "check_in_time": self.check_in_time.isoformat() if self.check_in_time else None,
            "check_out_time": self.check_out_time.isoformat() if self.check_out_time else None,
            "notes": self.notes
        }

    def __repr__(self) -> str:
        return f"<Attendance(id={self.id}, employee_id={self.employee_id}, date='{self.date}')>"