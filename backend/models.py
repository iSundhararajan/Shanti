from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class userManager(BaseUserManager):
    def create_user(self, phone, username, countryCode):
        if not username or not countryCode or not phone:
            raise ValueError('All the required fields must be provided')
        user = self.model(
            username = username,
            countryCode = countryCode,
            phone = phone
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, countryCode, password=None):
        user = self.create_user(phone, username=username, countryCode=countryCode)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False, default="user")
    countryCode = models.CharField(max_length=5, blank=False, null=False, default="+91")
    phone = models.CharField(max_length=11, unique=True, blank=False, null=False, default="0123456789")
    sessions = models.IntegerField(null=False, default=0)
    volunteerScore = models.IntegerField(null=False, default=0)
    password = models.CharField(null=True, blank=True, max_length=100)
    is_admin = models.BooleanField(null=False, default=False)
    is_staff = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)
    is_superuser = models.BooleanField(null=False, default=False)
    otp = models.CharField(null=True, blank=True, max_length=10)

    objects = userManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'countryCode']

    class Meta:
        ordering = ['volunteerScore', 'sessions']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Session(models.Model):
    topic = models.CharField(max_length=100, null=False, blank=False, default="peace")

    def __str__(self):
        return self.topic

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=False, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
