from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeProfile, Attendance, Salary, Leave, Department

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["employee_id", "photo", "department", "designation", "phone", "join_date"]

class ManagerEmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["user", "photo", "designation", "phone", "join_date"]

class EmployeeSelfProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ["photo", "phone"]

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["employee", "date", "status", "note"]

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ["employee", "month", "base_salary", "bonus", "deductions"]

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["start_date", "end_date", "reason"]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "manager"]
