from django.db import models

# Create your models here.

class TimeStampModel(models.Model):

    """ Definition of Abstract TimeStampModel """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RealCharField(models.CharField):

    """ Definition of RealCharField """
    
    def db_type(self, connection):
        varchar = super().db_type(connection)
        char = varchar.replace('varchar', 'char')
        return char



    
    