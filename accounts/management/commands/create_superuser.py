# backend/accounts/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import App

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a Super Admin user and default apps'

    def handle(self, *args, **options):
        # Create apps
        apps = ['HR', 'Volunteers', 'CRM', 'Leave']
        for name in apps:
            App.objects.get_or_create(name=name)
            self.stdout.write(f"✅ Created app: {name}")

        # Create Super Admin
        email = 'admin@nexorax.org'
        password = 'SecurePass123!'
        
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            user.is_superuser = True
            user.is_staff = True
            user.is_super_admin = True
            user.save()
            self.stdout.write(f"✅ Created Super Admin: {email}")
        else:
            self.stdout.write(f"ℹ️  Super Admin already exists: {email}")