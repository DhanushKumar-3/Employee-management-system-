from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import EmployeeProfile

@receiver(pre_save, sender=EmployeeProfile)
def set_employee_id(sender, instance, **kwargs):
    if instance.employee_id:
        return
    last = sender.objects.order_by("id").last()
    if not last or not last.employee_id:
        instance.employee_id = "EMP0001"
        return
    try:
        num = int(last.employee_id.replace("EMP", ""))
        instance.employee_id = f"EMP{num+1:04d}"
    except Exception:
        instance.employee_id = f"EMP{(last.id or 0)+1:04d}"
