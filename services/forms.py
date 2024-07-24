from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceProvider, Message

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

class ServiceProviderSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)
    years_of_experience = forms.IntegerField()
    average_rate = forms.DecimalField(max_digits=10, decimal_places=2)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            service_provider = ServiceProvider.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                description=self.cleaned_data['description'],
                years_of_experience=self.cleaned_data['years_of_experience'],
                average_rate=self.cleaned_data['average_rate'],
                profile_image=self.cleaned_data['profile_image']
            )
        return user

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']