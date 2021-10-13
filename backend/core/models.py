from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class City(models.Model):
    name = models.CharField(max_length=32)
    img = models.ImageField(upload_to="media/")

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    img = models.ImageField(upload_to="media/")
    is_live = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Reward(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    event = models.ForeignKey(Event, models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()


class QuestType(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    img = models.ImageField(upload_to="media/")
    polygon = models.PolygonField()
    importance = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Quest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quest_type = models.ForeignKey(QuestType, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(null=True)
