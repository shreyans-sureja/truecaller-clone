from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class RegisterUsers(models.Model):
    phone_number = PhoneNumberField(primary_key=True)
    name = models.CharField(max_length=50,blank=False,null=False)
    email = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,blank=False,null=False)

    def __str__(self):
        return self.name

class People(models.Model):
    phone_number = PhoneNumberField(primary_key=True)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

class PeopleDetails(models.Model):
    id = models.AutoField(primary_key=True)
    friend = models.ForeignKey(RegisterUsers, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=False,null=False)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.name