from django.db import models

# Create your models here.
device_types = (
    ('COMPUTER', "COMPUTER"),
    ('REPEATER', "REPEATER"),
)

class Device(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.CharField(choices=device_types,max_length=10)
    strength = models.IntegerField(default=5)
    connection = models.ManyToManyField(
        'self',
        related_name='children',
        symmetrical=False,
    )

    def __str__(self):
        return self.name


class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    connection = models.ManyToManyField(
        'self',
        related_name='children',
        symmetrical=False,
    )

