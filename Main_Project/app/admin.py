from django.contrib import admin
from .models import UserProfile,WorkerProfile,Work, Bid

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WorkerProfile)
admin.site.register(Work)
admin.site.register(Bid)

