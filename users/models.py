from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import RealCharField, TimeStampModel


class User(TimeStampModel, AbstractUser):

    """ Definition of User Model """

    POSITION_CHOICE =(
        ("DRIVER", "운전기사",),
        ("REPAIR", "수리기사",),
    )
    
    first_name = models.CharField("이름", max_length=100)
    last_name = models.CharField("성", max_length=100)
    email = models.EmailField("이메일", max_length=254, null=True, blank=True)
    phone = RealCharField("전화번호", max_length=13)
    position = RealCharField("역할", max_length=6, choices=POSITION_CHOICE)
    section = models.ForeignKey("sections.Section", verbose_name="담당구역", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
