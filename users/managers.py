from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError("Enter your username")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self.db)
        return user
