from django.contrib import admin
from .models import ServiceProvider, Service, Feedback, Chat, Message

admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(Feedback)
admin.site.register(Chat)
admin.site.register(Message)

# Register your models here.
