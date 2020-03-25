from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # username = models.CharField(max_length=50)
    # password = models.CharField(max_length=30)
    dob = models.DateField()
    # email = models.EmailField()
    phone = models.CharField(max_length=15)
    # is_active = models.BooleanField(default=False)

    ROLE = (
        (0, 'trainee'),
        (1, 'trainer'),
        (2, 'admin'),
    )

    role = models.IntegerField(choices=ROLE, default=0)
