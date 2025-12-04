from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
import csv
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import EmployeeProfile, Department, Attendance, Leave, Salary, Notification
from .forms import (
    UserCreateForm,
    EmployeeProfileForm,
    ManagerEmployeeProfileForm,
    EmployeeSelfProfileForm,
    AttendanceForm,
    SalaryForm,
    LeaveForm,
    DepartmentForm,
)
from .decorators import admin_required, manager_required, employee_required

def login_view(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            if user.is_superuser or user.groups.filter(name="Admin").exists():
                return redirect("admin_dashboard")
            if user.groups.filter(name="Manager").exists():
                return redirect("manager_dashboard")
            if user.groups.filter(name="Employee").exists():
                return redirect("employee_dashboard")
            return redirect("no_permission")
        messages.error(request, "Invalid username or password")
    return render(request, "employees/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def no_permission(request):
    return render(request, "employees/no_permission.html")

@login_required
@admin_required
def admin_dashboard(request):
    departments = Department.objects.all().annotate(emp_count=Count("employeeprofile"))
    emp_total = EmployeeProfile.objects.count()
    leave_pending = Leave.objects.filter(status="Pending").count()
    recent_notifs = Notification.objects.filter(user=request.user).order_by("-created")[:5]
    return render(request, "employees/admin_dashboard.html", {
        "departments": departments,
        "emp_total": emp_total,
        "leave_pending": leave_pending,
        "recent_notifs": recent_notifs,
    })

@login_required
@manager_required
def manager_dashboard(request):
    dept = getattr(request.user, "managed_department", None)
    employees = EmployeeProfile.objects.filter(department=dept) if dept else EmployeeProfile.objects.none()
    attendance_count = Attendance.objects.filter(employee__department=dept).count() if dept else 0
    avg_salary = Salary.objects.filter(employee__department=dept).aggregate(Avg("total_salary"))["total_salary__avg"] or 0
    leaves = Leave.objects.filter(employee__department=dept).order_by("-applied_on")[:10] if dept else []
    return render(request, "employees/manager_dashboard.html", {
        "department": dept,
        "employees": employees,
        "attendance_count": attendance_count,
        "avg_salary": avg_salary,
        "leaves": leaves,
    })

@login_required
@employee_required
def employee_dashboard(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    attendance = Attendance.objects.filter(employee=profile).order_by("-date")[:30]
    salary = Salary.objects.filter(employee=profile).order_by("-month")[:12]
    leaves = Leave.objects.filter(employee=profile).order_by("-applied_on")[:10]
    return render(request, "employees/employee_dashboard.html", {
        "profile": profile,
        "attendance": attendance,
        "salary": salary,
        "leaves": leaves,
    })

@login_required
@employee_required
def employee_profile_edit(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    if request.method == "POST":
        form = EmployeeSelfProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("employee_dashboard")
    else:
        form = EmployeeSelfProfileForm(instance=profile)
    return render(request, "employees/employee_profile_edit.html", {"form": form, "profile": profile})

# Admin employee management
@login_required
@admin_required
def employee_list(request):
    employees = EmployeeProfile.objects.select_related("user", "department").all()
    return render(request, "employees/employee_list.html", {"employees": employees})

@login_required
@admin_required
def employee_create(request):
    if request.method == "POST":
        user_form = UserCreateForm(request.POST)
        prof_form = EmployeeProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and prof_form.is_valid():
            user = user_form.save()
            emp_group, _ = Group.objects.get_or_create(name="Employee")
            user.groups.add(emp_group)
            profile = prof_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Employee created successfully.")
            return redirect("employee_list")
    else:
        user_form = UserCreateForm()
        prof_form = EmployeeProfileForm()
    return render(request, "employees/employee_create.html", {"user_form": user_form, "profile_form": prof_form})

@login_required
@admin_required
def employee_update(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employee_list")
    else:
        form = EmployeeProfileForm(instance=profile)
    return render(request, "employees/employee_update.html", {"form": form, "profile": profile})

@login_required
@admin_required
def employee_delete(request, pk):
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    if request.method == "POST":
        user = profile.user
        profile.delete()
        user.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect("employee_list")
    return render(request, "employees/employee_delete.html", {"profile": profile})


# Admin: department management
@login_required
@admin_required
def department_list(request):
    departments = Department.objects.all().annotate(emp_count=Count("employeeprofile"))
    return render(request, "employees/department_list.html", {"departments": departments})

@login_required
@admin_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department created.")
            return redirect("department_list")
    else:
        form = DepartmentForm()
    return render(request, "employees/department_form.html", {"form": form, "title": "Create Department"})

@login_required
@admin_required
def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated.")
            return redirect("department_list")
    else:
        form = DepartmentForm(instance=dept)
    return render(request, "employees/department_form.html", {"form": form, "title": "Edit Department"})

@login_required
@admin_required
def department_delete(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        dept.delete()
        messages.success(request, "Department deleted.")
        return redirect("department_list")
    return render(request, "employees/department_delete.html", {"department": dept})

# Admin: manager list/create
@login_required
@admin_required
def manager_list(request):
    mgr_group, _ = Group.objects.get_or_create(name="Manager")
    managers = User.objects.filter(groups=mgr_group)
    return render(request, "employees/manager_list.html", {"managers": managers})

@login_required
@admin_required
def manager_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            mgr_group, _ = Group.objects.get_or_create(name="Manager")
            user.groups.add(mgr_group)
            messages.success(request, "Manager created.")
            return redirect("manager_list")
    else:
        form = UserCreateForm()
    return render(request, "employees/manager_create.html", {"form": form})

# Manager: create employee (profile) for own department
@login_required
@manager_required
def manager_employee_create(request):
    dept = getattr(request.user, "managed_department", None)
    if not dept:
        messages.error(request, "You are not assigned to any department.")
        return redirect("manager_dashboard")
    if request.method == "POST":
        form = ManagerEmployeeProfileForm(request.POST, request.FILES)
        # Limit choices for security
        form.fields["user"].queryset = User.objects.filter(groups__name="Employee").exclude(employeeprofile__isnull=False)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.department = dept
            profile.save()
            messages.success(request, "Employee profile created for your department.")
            return redirect("manager_dashboard")
    else:
        form = ManagerEmployeeProfileForm()
        form.fields["user"].queryset = User.objects.filter(groups__name="Employee").exclude(employeeprofile__isnull=False)
    return render(request, "employees/manager_employee_create.html", {"form": form, "department": dept})

# Manager actions: attendance, salary, leave approval
@login_required
@manager_required
def mark_attendance(request, emp_id):
    profile = get_object_or_404(EmployeeProfile, pk=emp_id)
    if request.user.managed_department != profile.department and not request.user.is_superuser:
        messages.error(request, "You are not allowed to mark attendance for this employee.")
        return redirect("manager_dashboard")
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance saved.")
            return redirect("manager_dashboard")
    else:
        form = AttendanceForm(initial={"employee": profile})
    return render(request, "employees/mark_attendance.html", {"form": form, "profile": profile})

@login_required
@manager_required
def process_salary(request, emp_id):
    profile = get_object_or_404(EmployeeProfile, pk=emp_id)
    if request.user.managed_department != profile.department and not request.user.is_superuser:
        messages.error(request, "You are not allowed to process salary for this employee.")
        return redirect("manager_dashboard")
    if request.method == "POST":
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary processed.")
            return redirect("manager_dashboard")
    else:
        form = SalaryForm(initial={"employee": profile})
    return render(request, "employees/process_salary.html", {"form": form, "profile": profile})

@login_required
@manager_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.user.managed_department != leave.employee.department and not request.user.is_superuser:
        messages.error(request, "You are not allowed to modify this leave.")
        return redirect("manager_dashboard")
    action = request.GET.get("action")
    if action in ["Approve", "Reject"]:
        leave.status = "Approved" if action == "Approve" else "Rejected"
        leave.save()
        messages.success(request, f"Leave {leave.status}.")
    return redirect("manager_dashboard")

# Employee: apply leave
@login_required
@employee_required
def apply_leave(request):
    profile = get_object_or_404(EmployeeProfile, user=request.user)
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = profile
            leave.save()
            messages.success(request, "Leave applied.")
            return redirect("employee_dashboard")
    else:
        form = LeaveForm()
    return render(request, "employees/apply_leave.html", {"form": form})

# Exports
@login_required
def export_attendance_csv(request):
    qs = Attendance.objects.select_related("employee__user")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=attendance.csv"
    writer = csv.writer(response)
    writer.writerow(["EMP ID", "Name", "Date", "Status", "Note"])
    for a in qs:
        writer.writerow([a.employee.employee_id, a.employee.user.get_full_name(), a.date, a.status, a.note])
    return response

@login_required
def export_salary_excel(request):
    qs = Salary.objects.select_related("employee__user")
    wb = Workbook()
    ws = wb.active
    ws.title = "Salary"
    ws.append(["EMP ID", "Name", "Month", "Base", "Bonus", "Deductions", "Total"])
    for s in qs:
        ws.append([
            s.employee.employee_id,
            s.employee.user.get_full_name(),
            s.month,
            float(s.base_salary),
            float(s.bonus),
            float(s.deductions),
            float(s.total_salary),
        ])
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="salary.xlsx"'
    return response

@login_required
def export_salary_pdf(request):
    qs = Salary.objects.select_related("employee__user")
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Salary Report")
    y -= 40
    p.setFont("Helvetica", 10)
    p.drawString(30, y, "EMP ID")
    p.drawString(100, y, "Name")
    p.drawString(260, y, "Month")
    p.drawString(330, y, "Total")
    y -= 20
    for s in qs:
        p.drawString(30, y, str(s.employee.employee_id))
        p.drawString(100, y, s.employee.user.get_full_name())
        p.drawString(260, y, s.month)
        p.drawString(330, y, str(s.total_salary))
        y -= 18
        if y < 50:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")

# FullCalendar attendance events
@login_required
def attendance_events(request):
    qs = Attendance.objects.select_related("employee__user")[:1000]
    events = []
    for a in qs:
        events.append({
            "title": f"{a.employee.employee_id} - {a.status}",
            "start": str(a.date),
            "allDay": True,
        })
    return JsonResponse(events, safe=False)

# Notifications
@login_required
def notifications_list(request):
    notifs = Notification.objects.filter(user=request.user).order_by("-created")[:50]
    return render(request, "employees/notifications.html", {"notifications": notifs})

@login_required
def mark_notification_read(request, nid):
    notif = get_object_or_404(Notification, pk=nid, user=request.user)
    notif.read = True
    notif.save()
    return redirect("notifications")
