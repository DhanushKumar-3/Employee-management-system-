from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create basic groups: Admin, Manager, Employee"

    def handle(self, *args, **options):
        for name in ["Admin", "Manager", "Employee"]:
            Group.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Groups ensured: Admin, Manager, Employee"))
