from django.db import models

# Create your models here.
# type = (
#         (1, 'Flat'),
#         (2, 'Percentage'),
#     )

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.name


class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.name
class Vat(models.Model):
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    # status = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.percentage

class Commission(models.Model):
    # type = models.IntegerField(choices=type, default=1)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    # status = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.percentage