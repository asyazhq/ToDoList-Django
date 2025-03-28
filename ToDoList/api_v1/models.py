from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class TodoListModel(models.Model):
    """
        Describe the model of a Task and generate an ORM
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # Optional
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Predefined choices
    owner = models.ForeignKey('UserModel', related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        """
            Some optional field like ordering to sort the table
        """
        ordering = ('created',)

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name='', last_name='', **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=False, default="")  # Required field
    last_name = models.TextField(blank=True, null=True, default="")  # Optional field
    username = models.CharField(max_length=50, unique=True, blank=False, default="")  # Unique & required
    password = models.CharField(max_length=128, blank=False)  # Required, will be hashed
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.username
