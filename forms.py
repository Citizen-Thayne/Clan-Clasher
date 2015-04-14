from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from ClanClasher.models import Chief


class ChiefForm(forms.ModelForm):
    name = forms.CharField(label='Chief Name', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Chief
        fields = ('name', 'level')


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=75, widget=forms.TextInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ("email",)

    def save(self, commit=True):
        # Ensure that the username is set to the email address provided,
        # so the user_save_patch() will keep things in sync.
        self.instance.username = self.instance.email
        return super(MyUserCreationForm, self).save(commit=commit)


class MyUserAuthenticationForm(AuthenticationForm):
    pass
    # class Meta:
    # model = get_user_model()




