from django.contrib import admin
from . import models

admin.site.register(models.Employee)
admin.site.register(models.Office)
admin.site.register(models.Region)
admin.site.register(models.State)
admin.site.register(models.Provider)
admin.site.register(models.Lead)
