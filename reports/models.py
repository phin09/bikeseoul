from django.db import models
from core.models import TimeStampModel, RealCharField


class Report(TimeStampModel):

    """ Definition of Report Model """

    CATEGORY_CHOICE = (
        ('BIKE', "자전거",),
        ("RACK", "거치대",),
        ("ETC", "기타",),
    )
    PRIORITY_CHOICE = (
        ('HIGH', "매우 중요"),
        ('MID', "중요"),
        ('LOW', "보통"),
    )
    
    category = RealCharField("분류", max_length=4, choices=CATEGORY_CHOICE)
    description = models.CharField("상세 내용", max_length=2000)
    priority = RealCharField("우선순위", max_length=4, choices=PRIORITY_CHOICE)
    station = models.ForeignKey("stations.Station", verbose_name="대여소", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", verbose_name="신고자", on_delete=models.CASCADE)

    class Meta:
        db_table = "reports"
        verbose_name = "고장 신고"
        verbose_name_plural = "고장 신고"

        

    





