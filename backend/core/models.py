from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.geos import Point
from users.models import User


class City(models.Model):
    name = models.CharField(max_length=32)
    img = models.ImageField(upload_to="media/")

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    img = models.ImageField(upload_to="media/")
    is_live = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class QuestType(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    img = models.ImageField(upload_to="media/")
    polygon = models.PolygonField(null=True)
    importance = models.IntegerField(
        default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Quest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(QuestType, on_delete=models.CASCADE)
    finish_date = models.DateTimeField(null=True)


class Report(models.Model):
    class Category(models.TextChoices):
        DANGER = ("D", "Niebezpieczeństwo")
        HELPER = ("H", "Usprawnienie")
        OTHER = ("O", "Inne")

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=1, choices=Category.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.PointField(default=Point(0, 0))

    def __str__(self) -> str:
        return self.title