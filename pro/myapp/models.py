import os
import pandas as pd
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.
class customer(models.Model):
    Fname = models.CharField(max_length=20)
    Lname = models.CharField(max_length=20)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=20)

    def __str__(self):
        return self.Fname

class extended(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)
@receiver(pre_delete, sender = User)
def pic_remove(sender, instance, **kwargs):
    try:
        os.remove(instance.extended.img.path)
    except:
        pass

@receiver(pre_delete, sender=User)
def log(sender, instance, **kwargs):
    user_log = [{
        'Name of User': instance.get_full_name(),
        'User Id': instance.id,
        'DateTime': datetime.now()
    }]
    df = pd.DataFrame(user_log)
    df.to_csv('user_log.csv', header=False, sep="|", index=False, mode='a')
