from django.db import models


class Bus(models.Model):
    info = models.CharField(max_length=255, null=True)
    num_seats = models.IntegerField()

    class Meta:
        verbose_name_plural = "buses"

    @property
    def is_mini(self):
        return self.num_seats <= 10

    def __str__(self):
        return self.info
