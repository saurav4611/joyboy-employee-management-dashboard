1. Clone the repository

git clone https://github.com/YOUR-USERNAME/joyboy-emplyoee-management-dashboard.git
cd joyboy-flow

2. Create and activate a virtual environment

####In bash
python -m venv venv
# On Windows
venv\Scripts\activate
3. Install dependencies

####In bash
pip install -r requirements.txt

4. Configure Environment

####In bash
# Copy the example environment file
# On Windows
copy .env.example .env

5. Run the application

####In bash
python main.py


PROJECT STRUCTURE
joyboy-flow/
├── main.py               
# Application entry point
├── config.py             
# Environment & path configuration
├── database/              
# Database session & data seeding
├── models/                
# SQLAlchemy ORM models
├── controllers/           
# UI to Service routing logic
├── services/              
# Business logic & DB queries
├── ui/                   
# PySide6 GUI components & pages
│   ├── components/        
# Reusable widgets (Sidebar, Cards)
│   └── dialogs/          
# Input forms (Employee Dialog)
├── utils/               
# Logging, Error handling, Exporters
└── assets/              
# Icons and static files
