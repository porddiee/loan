Loan Management System

This is a simple Loan Management System built using Django. It allows users to register, request loans, and make payments. Admin users can approve or reject loans. The system is designed for small-scale use and is great for learning how to manage users, forms, and models in Django.

🚀 Features
User registration and login
Admin dashboard
Users can request loans
Admins can approve or reject loan requests
Users can make payments
Loan status tracking
Simple Bootstrap-based interface

🔧 Technologies Used
Python 3
Django
SQLite (default database)
HTML, CSS, JavaScript
Bootstrap

📂 Project Structure
loan/
├── loan/                  # Main project folder
│   ├── settings.py        # Django settings
│   └── urls.py            # Project-level routes
├── loans/                 # App for loan functionality
│   ├── models.py          # Database models
│   ├── views.py           # Logic for handling requests
│   ├── forms.py           # Forms for user input
│   └── templates/         # HTML templates
│       └── loans/
├── manage.py              # Django's CLI tool
└── db.sqlite3             # SQLite database file

🖥️ How to Run the Project
Prerequisites
Make sure Python and pip are installed on your system.

Installation
Clone the repository

git clone https://github.com/porddiee/loan.git
cd loan
Create a virtual environment (optional but recommended)


python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install dependencies

pip install -r requirements.txt
Apply migrations

python manage.py makemigrations
python manage.py migrate
Create a superuser for admin access

python manage.py createsuperuser
Run the development server

python manage.py runserver
Open your browser and go to http://127.0.0.1:8000

🔐 Admin Access
Log in to the admin panel at http://127.0.0.1:8000/admin using the superuser credentials you created.

📸 Screenshots (Optional)
You can add screenshots of your user dashboard, admin panel, loan request form, etc. here.

🛠️ Future Improvements
Soon..

📄 License
This project is for educational purposes.
