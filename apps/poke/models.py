from __future__ import unicode_literals
from django.db import models
from ..loginreg.models import User

# Create your models here.
class PokeManager(models.Manager):
    def poke(self, poker, pokee):
        p = self.all().filter(poker=poker, pokee=pokee)
        if not p:
            p = self.create(poker=poker, pokee=pokee, count=1)
            p.save()
        else:
            p[0].count += 1
            p[0].save()
        pokee.pokes += 1
        pokee.save()
        return True
    def getPokeList(self, user):
        return self.all().filter(pokee=user).order_by('-count')
class Poke(models.Model):
    poker = models.ForeignKey(User, related_name='poker')
    pokee = models.ForeignKey(User, related_name='pokee')
    count = models.IntegerField()
    manager = PokeManager()
