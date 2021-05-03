from django.db import models

from core.models import TimeStampModel, RealCharField


class Station(TimeStampModel):

    """ Definition of Station Model """

    STATUS_CHOICE = (
        ("NORMAL", "정상",),
        ("REPAIR", "수리중",),
        ("CLOSED", "폐쇄",),
    )

    code = RealCharField("코드", unique=True, max_length=9)
    name = models.CharField("이름", max_length=100)
    lot_address = models.CharField("지번 주소", max_length=100, null=True, blank=True)
    street_address = models.CharField("도로명 주소", max_length=100)
    detail_address = models.CharField("상세 주소", max_length=100, null=True, blank=True)
    latitude = models.DecimalField("위도", max_digits=9, decimal_places=6)
    longitude = models.DecimalField("경도", max_digits=9, decimal_places=6)
    rack_cnt = models.IntegerField("거치대 수")
    status = RealCharField("상태", choices=STATUS_CHOICE, max_length=6, default="NORMAL")
    is_lcd = models.BooleanField("LCD 따릉이 거치소 여부", null=True, blank=True)

    class Meta:
        db_table = "stations"
        verbose_name = "대여소"
        verbose_name_plural = "대여소 이름"


class StationLog(TimeStampModel):

    """ Definition of StationLog Model """

    total_cnt = models.IntegerField("총 자전거 거치 대수", default=0)
    lcd_cnt = models.IntegerField("qr 자전거 거치 대수", default=0)
    qr_cnt = models.IntegerField("lcd 자전거 거치 대수", default=0)
    sprout_cnt = models.IntegerField("새싹 자전거 거치 대수", default=0)
    station = models.ForeignKey("stations.Station", verbose_name="대여소", on_delete=models.CASCADE)

    class Meta:
        db_table = "station_logs"
        ordering = ["created_at",]
