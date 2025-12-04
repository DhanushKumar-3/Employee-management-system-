from django.contrib import admin
from .models import Department, EmployeeProfile, Attendance, Leave, Salary, Notification

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "manager")

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "user", "department", "designation")

admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Salary)
admin.site.register(Notification)
