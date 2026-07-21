import random
from datetime import date, timedelta, time
from database.session import DatabaseManager
from models.employee import Employee
from models.attendance import Attendance
from utils.logger import get_logger

logger = get_logger("database.seed")

FIRST_NAMES = [
    "Rahul", "Priya", "Amit", "Neha", "Arjun", "Pooja", "Ravi", "Anjali",
    "Vikram", "Sneha", "Sanjay", "Kavita", "Rajesh", "Sunita", "Manoj", "Shreya",
    "Rakesh", "Meena", "Suresh", "Kiran", "Deepak", "Nisha", "Anand", "Komal",
    "Vivek", "Rekha", "Ashok", "Seema", "Naveen", "Alka", "Ajay", "Ritika",
    "Harish", "Divya", "Prakash", "Jyoti", "Santosh", "Payal", "Karan", "Radhika",
    "Mahesh", "Geeta", "Lokesh", "Swati", "Balaji", "Lata", "Shiv", "Monika",
    "Ganesh", "Parvati"
]

LAST_NAMES = [
    "Sharma", "Verma", "Singh", "Yadav", "Patel", "Reddy", "Iyer", "Nair",
    "Chopra", "Kapoor", "Mehta", "Joshi", "Kulkarni", "Bose", "Banerjee", "Mukherjee",
    "Das", "Ghosh", "Chatterjee", "Roy", "Gupta", "Malhotra", "Khanna", "Aggarwal",
    "Jain", "Saxena", "Srivastava", "Pandey", "Mishra", "Tripathi", "Dubey", "Tiwari",
    "Bhatt", "Desai", "Parmar", "Solanki", "Rastogi", "Bhatnagar", "Chaudhary", "Thakur",
    "Gill", "Sandhu", "Kaur", "Ahluwalia", "Grover", "Arora", "Bhatia", "Sodhi",
    "Menon", "Pillai"
]

DEPARTMENTS = [
    "Engineering", "Marketing", "Sales", "Human Resources", 
    "Finance", "Operations", "Customer Support", "Research & Development"
]

POSITIONS = [
    "Junior Developer", "Senior Developer", "Tech Lead", "Manager", 
    "Director", "Analyst", "Coordinator", "Specialist", "Intern", 
    "Architect", "Consultant", "Administrator"
]

def seed_database() -> None:
    session = DatabaseManager.get_session()
    try:
        if session.query(Employee).count() > 0:
            logger.info("Database already contains data. Skipping seed.")
            return
            
        logger.info("Seeding database with sample data...")
        random.seed(42)
        employees = []
        
        for i in range(1, 51):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            emp = Employee(
                employee_code=f"EMP{i:04d}",
                first_name=first,
                last_name=last,
                email=f"{first.lower()}.{last.lower()}{i}@joyboyflow.com",
                phone=f"555-{random.randint(1000, 9999)}",
                department=random.choice(DEPARTMENTS),
                position=random.choice(POSITIONS),
                salary=round(random.uniform(35000, 140000), 2),
                hire_date=date(random.randint(2018, 2024), random.randint(1, 12), random.randint(1, 28)),
                is_active=random.random() > 0.1
            )
            employees.append(emp)
            session.add(emp)
            
        session.flush()
        
        today = date.today()
        for emp in employees:
            for days_ago in range(30):
                att_date = today - timedelta(days=days_ago)
                if att_date.weekday() >= 5: 
                    continue
                is_present = random.random() > 0.12
                att = Attendance(
                    employee_id=emp.id,
                    date=att_date,
                    status="present" if is_present else "absent",
                    check_in_time=time(9, random.randint(0, 30)) if is_present else None,
                    check_out_time=time(17, random.randint(0, 30)) if is_present else None,
                    notes="" if is_present else random.choice(["", "Sick leave", "Personal leave", "Vacation", "Unauthorized absence"])
                )
                session.add(att)
                
        session.commit()
        logger.info("Database seeding complete. Created 50 employees and 30 days of attendance.")
    except Exception as e:
        session.rollback()
        logger.error("Failed to seed database: %s", str(e))
        raise
    finally:
        session.close()