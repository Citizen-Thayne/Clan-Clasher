from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from emailusernames.utils import user_exists

from ClanClasher.models import Chief, MyUser


class ChiefForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = ('name', 'level')


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=("Email"), max_length=75)

    class Meta:
        model = get_user_model()
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     User = get_user_model()
    #     user_lookup = User(email=email)
    #     if user_lookup is not None:
    #         raise forms.ValidationError("A user with that email already exists.")
    #      # if user_exists(email):
    #     #     raise forms.ValidationError("A user with that email already exists.")
    #     return email

    def save(self, commit=True):
        # Ensure that the username is set to the email address provided,
        # so the user_save_patch() will keep things in sync.
        self.instance.username = self.instance.email
        return super(MyUserCreationForm, self).save(commit=commit)





