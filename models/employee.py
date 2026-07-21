from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, func
from sqlalchemy.orm import relationship
from database.base import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_code = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    department = Column(String(100), nullable=False, index=True)
    position = Column(String(150), nullable=True)
    salary = Column(Float, nullable=True, default=0.0)
    hire_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def status_label(self) -> str:
        return "Active" if self.is_active else "Inactive"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "employee_code": self.employee_code,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "position": self.position,
            "salary": self.salary if self.salary is not None else 0.0,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "is_active": self.is_active,
            "status_label": self.status_label
        }

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, code='{self.employee_code}')>"