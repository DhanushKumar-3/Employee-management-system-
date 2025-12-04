📘 Employee Management System (EMS)

A complete, production-ready Employee Management System (EMS) with Admin, Manager, and Employee dashboards built using Django 6, Python 3.14, Bootstrap 5, and Chart.js. Packed with role-based permissions, salary + attendance management, notifications, fullcalendar, export tools, and modern UI/UX.

📸 Screenshots

⚠️ Replace the placeholder image links (/screenshots/...) with your actual screenshots.

🔐 Login Page

👑 Admin Dashboard

👨‍💼 Manager Dashboard

👨‍🔧 Employee Dashboard

📅 Attendance Calendar

💰 Salary Chart

🚀 Features
👑 Admin Features

Manage Departments

Assign Managers

CRUD for Managers

CRUD for Employees

Export Attendance (CSV)

Export Salary (Excel/PDF)

System-wide notifications

Full control dashboard

👨‍💼 Manager Features

Manage employees in their department

Add/update/delete employees

Mark attendance

Process salary + bonuses/deductions

Approve/Reject leave requests

View salary/attendance history

Receive notifications

👨‍🔧 Employee Features

View profile (department, manager, join date)

Edit profile (photo, phone)

Attendance history (charts + calendar)

Salary history (charts)

Apply for leave

View notifications

🎨 UI / UX Features

Modern Bootstrap Dashboard

Smooth sliding animations

Parallax header & particle effects (optional)

Dark/Light theme with localStorage

Responsive UI

Chart.js graphs

FullCalendar attendance view

Animated toast notifications

📁 Project Structure
employee_mgmt/
│
├── employees/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── templatetags/group_tags.py
│   └── templates/employees/
│
├── employee_mgmt/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── media/
├── requirements.txt
└── manage.py

🔧 Installation
1️⃣ Create a virtual environment
python3.14 -m venv env

2️⃣ Activate

Windows

env\Scripts\activate


Linux/macOS

source env/bin/activate

3️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create Superuser
python manage.py createsuperuser

6️⃣ Initialize default groups
python manage.py init_roles

7️⃣ Start server
python manage.py runserver

🔑 URLs
Feature	URL
Login	/login/
Admin Dashboard	/admin/dashboard/
Manager Dashboard	/manager/dashboard/
Employee Dashboard	/employee/dashboard/
Django Admin	/admin-site/
📤 Export Tools
Feature	Format	URL
Attendance	CSV	/export/attendance/csv/
Salary	Excel	/export/salary/excel/
Salary	PDF	/export/salary/pdf/
🔔 Notifications

Admin messages appear for both Managers and Employees.
Toast messages appear after all successful operations.

🔒 Role Access Control
Role	Access
Admin	Full access
Manager	Only employees in their department
Employee	View-only + leaves

Custom decorators:

@admin_required
@manager_required
@employee_required

🧪 Creating Test Accounts

Use /admin-site/ or EMS Admin UI to create:

Managers

Employees

Departments

📝 License

This project is open-source under the MIT License.

❤️ Want more improvements?

I can add:

REST API (Django REST Framework)

Mobile app (Flutter/React Native)

Email/SMS alerts

Payroll templates

Auto attendance generation

Multi-company support

Facial recognition attendance

QR-code login

Just ask!
