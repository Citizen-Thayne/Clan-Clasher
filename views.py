from django.contrib.auth import logout
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from emailusernames.forms import EmailUserCreationForm, EmailAuthenticationForm
from ClanClasher.forms import ChiefForm, MyUserCreationForm
from ClanClasher.models import Profile, Chief
from django.contrib import auth


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        user_form = MyUserCreationForm(request.POST)
        chief_form = ChiefForm(request.POST)

        if user_form.is_valid() and chief_form.is_valid():
            new_user = user_form.save()
            new_chief = chief_form.save()
            new_profile = Profile(chief=new_chief, user=new_user).save()
            # Profile.objects.create(chief=new_chief, user=new_user)
            return render(request, 'index.html')
    else:
        user_form = EmailUserCreationForm
        chief_form = ChiefForm
    return render(request, 'register.html', {'user_form': user_form, 'chief_form': chief_form})


def login(request):
    if request.method == 'POST':
        login_form = EmailAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth.login(request,user)
            return render(request, 'index.html')
            # user = auth.authenticate(email=login_form.data.email, password=login_form.data.password1)
            # if user:
            #     auth.login(request, user)
            #     return render(request, 'index.html')
    else:
        login_form = EmailAuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out')
    return render(request, 'index.html', )


def index(request):
    return render(request, 'index.html')


class ChiefDetailView(DetailView):
    model = Chief








