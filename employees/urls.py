from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("no-permission/", views.no_permission, name="no_permission"),

    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/departments/", views.department_list, name="department_list"),
    path("admin/departments/create/", views.department_create, name="department_create"),
    path("admin/departments/<int:pk>/edit/", views.department_update, name="department_update"),
    path("admin/departments/<int:pk>/delete/", views.department_delete, name="department_delete"),

    path("admin/managers/", views.manager_list, name="manager_list"),
    path("admin/managers/create/", views.manager_create, name="manager_create"),

    path("manager/dashboard/", views.manager_dashboard, name="manager_dashboard"),
    path("employee/dashboard/", views.employee_dashboard, name="employee_dashboard"),
    path("employee/profile/edit/", views.employee_profile_edit, name="employee_profile_edit"),

    path("employees/", views.employee_list, name="employee_list"),
    path("employees/create/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/update/", views.employee_update, name="employee_update"),
    path("employees/<int:pk>/delete/", views.employee_delete, name="employee_delete"),

    path("manager/employees/create/", views.manager_employee_create, name="manager_employee_create"),
    path("manager/attendance/<int:emp_id>/", views.mark_attendance, name="mark_attendance"),
    path("manager/salary/<int:emp_id>/", views.process_salary, name="process_salary"),
    path("manager/leave/<int:leave_id>/", views.approve_leave, name="approve_leave"),

    path("employee/apply-leave/", views.apply_leave, name="apply_leave"),

    path("export/attendance/csv/", views.export_attendance_csv, name="export_attendance_csv"),
    path("export/salary/excel/", views.export_salary_excel, name="export_salary_excel"),
    path("export/salary/pdf/", views.export_salary_pdf, name="export_salary_pdf"),

    path("calendar/events/", views.attendance_events, name="attendance_events"),

    path("notifications/", views.notifications_list, name="notifications"),
    path("notifications/read/<int:nid>/", views.mark_notification_read, name="mark_notification_read"),
]
