from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(WorkerProfile)
admin.site.register(Work)
admin.site.register(Bid)
admin.site.register(Rating)

