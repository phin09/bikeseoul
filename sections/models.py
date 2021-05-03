from django.db import models

from core.models import TimeStampModel


class Section(TimeStampModel):

    """ Definition of Section Model """

    name = models.CharField("이름", max_length=50, help_text="해당 지역의 이름을 적어 주세요.")
    description = models.CharField("설명", max_length=1000, null=True, blank=True)
    stations = models.ManyToManyField("stations.Station", verbose_name="대여소")


    class Meta:
        db_table = "sections"
        verbose_name = "담당지역"
        verbose_name_plural = "담당지역"
