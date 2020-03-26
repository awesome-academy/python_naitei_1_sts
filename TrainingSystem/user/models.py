from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    dob = models.DateField(null=True)
    phone = models.CharField(null=True, max_length=15)

    ROLE = (
        (0, 'trainee'),
        (1, 'trainer'),
        (2, 'admin'),
    )

    role = models.IntegerField(choices=ROLE, default=0)
