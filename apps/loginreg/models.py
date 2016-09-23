from __future__ import unicode_literals
from django.db import models
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self, form_data):
        errors = []
        if len(form_data['name']) < 2:
            errors.append('Name must be at least two characters!')
        if len(form_data['alias']) < 2:
            errors.append('Alias must be at least two characters!')
        if not all(x.isalpha() or x.isspace() for x in form_data['name']):
            errors.append('Name must be alphabetic!')
        if len(form_data['email']) == 0:
            errors.append('Email is required!')
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Invalid email!')
        if len(form_data['password']) < 8:
            errors.append('Password must be at least eight characters!')
        if form_data['password'] != form_data['confirmation']:
            errors.append('Password and confirmation must match!')
        if form_data['dob'] > datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'):
            errors.append('Date of birth cannot be in the future!')
        if len(errors) is not 0:
            return (False, errors)
        else:
            u = self.create(name=form_data['name'], alias=form_data['alias'], email=form_data['email'], password=bcrypt.hashpw(form_data['password'].encode('utf-8'), bcrypt.gensalt()), date_of_birth=form_data['dob'])
            u.save()
            return (True, u)

    def login(self, form_data):
        errors = []
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append('Invalid email!')
            return (False, errors)
        u = self.all().filter(email=form_data['email'])[:1]
        if not u[0]:
            errors.append('Invalid email or password')
            return (False, errors)
        if not bcrypt.hashpw(form_data['password'].encode('utf-8'), u[0].password.encode('utf-8')) == u[0].password:
            errors.append('Invalid email or password')
            return (False, errors)
        else:
            return (True, u[0])

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    pokes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    manager = UserManager()
