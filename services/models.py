from django.db import models
from django.contrib.auth.models import User

class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    years_of_experience = models.IntegerField()
    average_rate = models.DecimalField(max_digits=10, decimal_places=2)
    profile_image = models.ImageField(upload_to='profile_images/')
    
    def __str__(self):
        return self.name

class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/')
    
    def __str__(self):
        return self.title

class Feedback(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    
    def __str__(self):
        return f'{self.service.title} - {self.customer.username}'
    
class Chat(models.Model):
    customer = models.ForeignKey(User, related_name='customer_chats', on_delete=models.CASCADE)
    provider = models.ForeignKey(User, related_name='provider_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat between {self.customer.username} and {self.provider.username}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} at {self.timestamp}'
