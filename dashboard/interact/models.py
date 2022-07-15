from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()

class State(models.Model):
    state = models.CharField(max_length=2, blank=True, null=False)

    def __str__(self):
        return self.state

class Status(models.Model):
    status = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.status

class Provider(models.Model):
    company_name = models.CharField(max_length=64, blank=True, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=False)

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return reverse(
            "market:provider",
            kwargs = {
                "pk": self.pk
            }
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'providers'


class Region(models.Model):
    name = models.CharField(max_length=64,blank=False,null=False,unique=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = 'regions'

    def get_absolute_url(self):
        return reverse(
            "market:region_leads",
            kwargs = {
                "pk": self.pk
            }
        )


class Office(models.Model):
    name = models.CharField(max_length=64,blank=False,null=False,unique=False)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "market:office-settings",
            kwargs = {
                "pk": self.pk
            }
        )

    class Meta:
        verbose_name = "Office"
        verbose_name_plural = "Offices"
        ordering = ['name']
        db_table = 'offices'

class Employee(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=False)
    office = models.ForeignKey(Office, null=False, blank=True, on_delete=models.DO_NOTHING, default=1)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.DO_NOTHING, default=1)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "market:leads",
            kwargs = {
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ['name']
        db_table = 'employees'

class Zip(models.Model):
    zip_code = models.CharField(max_length=10, blank=False, null=False)
    state = models.CharField(max_length=2, blank=False, null=False, default='US')
    zip_extension = models.CharField(max_length=10, blank=True, null=False)

    def __int__(self):
        return self.zip_code

class Lead(models.Model):
    #Required Fields
    first_name = models.CharField(max_length=64, blank=True, null=False)
    last_name = models.CharField(max_length=64, blank=True, null=False)
    phone = models.CharField(max_length=32, blank=True, null=False)
    email = models.EmailField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=False)
    city = models.CharField(max_length=64, blank=True, null=False)
    state = models.ForeignKey(State, related_name="lead_state",null=True, blank=True, on_delete=models.PROTECT)
    zip = models.CharField(max_length=12, blank=True, null=False)
    provider = models.ForeignKey(Provider, related_name="provider_name", null=False, blank=True, default=None, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, related_name="employee_name", null=True, blank=True, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, null=False, blank=True, on_delete=models.DO_NOTHING, default=1)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.DO_NOTHING, default=1)
    appt_date = models.DateField(blank=True, null=True)
    appt_time = models.TimeField(blank=True, null=True)
    signed = models.DateField(blank=True, null=True)
    approved = models.DateField(blank=True, null=True)
    m1 = models.DateField(blank=True, null=True)
    m2 = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=False)
    lat = models.CharField(max_length=64,blank=True,null=True)
    lng = models.CharField(max_length=64,blank=True,null=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse(
            "market:single-lead",
            kwargs = {
                "employee_slug": self.employee.slug,
                "office_slug": self.manager.slug,
                "pk": self.pk
            }
        )

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ['-created']
        db_table = 'leads'
