from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, ServiceProviderSignUpForm
from .models import ServiceProvider, Chat, Message
from django.views.generic import ListView

from django.contrib.auth.models import User
from .forms import MessageForm


def home(request):
    providers = ServiceProvider.objects.all()
    return render(request, 'services/home.html', {'providers': providers})

@login_required
def provider_detail(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    return render(request, 'services/provider_detail.html', {'provider': provider})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def service_provider_signup(request):
    if request.method == 'POST':
        form = ServiceProviderSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = ServiceProviderSignUpForm()
    return render(request, 'registration/service_provider_signup.html', {'form': form})

@login_required
def start_chat(request, provider_id):
    provider = get_object_or_404(User, id=provider_id)
    chat, created = Chat.objects.get_or_create(customer=request.user, provider=provider)

    return redirect('chat_detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user != chat.customer and request.user != chat.provider:
        return redirect('home')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    messages = chat.messages.all()

    return render(request, 'services/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form,
    })

class ChatListView(ListView):
    model = Chat
    template_name = 'services/chat_list.html'
    
    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(customer=user) | Chat.objects.filter(provider=user)