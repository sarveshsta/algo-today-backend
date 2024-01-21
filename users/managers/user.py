from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    class UserManager is called by the django auth.
    Whenever we create authenticate superuser with email and password, username is not needed for superuser.
    - We create authenticate user with `email` or `mobile` and `password`.
    - `username` is not required.
    """

    use_in_migrations = True

    # function for create user or superuser
    def _create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        else:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function for add normal user's other field
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        user = self._create_user(email=email, password=password, **extra_fields)
        # Create the user profile for the user
        from users.models.profile import UserProfile

        UserProfile.objects.create(user=user)

        return user

    # function for add superusers other field
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # display error message if is_staff and is_superuser is false for superuser.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True.")
        return self._create_user(email=email, password=password, **extra_fields)
