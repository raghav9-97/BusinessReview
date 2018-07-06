from django.db import models
from django.contrib.auth.models import AbstractUser

class UserDefined(AbstractUser):
    USER_TYPE_ACCOUNTADMIN = 0
    USER_TYPE_MANAGER = 1
    USER_TYPES = (
        (USER_TYPE_ACCOUNTADMIN, "Account Admin"),
        (USER_TYPE_MANAGER, "Manager"),
    )
    user_type = models.IntegerField(choices=USER_TYPES,null=True)
    admin = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
