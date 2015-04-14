from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.views.generic.list import ListView

from ClanClasher.forms import ChiefForm, MyUserCreationForm, MyUserAuthenticationForm
from ClanClasher.models import Profile, Chief


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        user_form = MyUserCreationForm(request.POST)
        chief_form = ChiefForm(request.POST)

        if user_form.is_valid() and chief_form.is_valid():
            new_user = user_form.save()
            new_chief = chief_form.save()
            new_profile = Profile(chief=new_chief, user=new_user).save()
            return render(request, 'index.html')
    else:
        user_form = MyUserCreationForm()
        chief_form = ChiefForm
    return render(request, 'register.html', {'user_form': user_form, 'chief_form': chief_form})


def login(request):
    if request.method == 'POST':
        login_form = MyUserAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth.login(request, user)
            return render(request, 'index.html')
    else:
        login_form = MyUserAuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return render(request, 'index.html', )


def index(request):
    return render(request, 'index.html')


class ChiefDetailView(DetailView):
    model = Chief


class ChiefListView(ListView):
    model = Chief


class ClanDetailView(DetailView):
    model = Chief
