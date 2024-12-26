from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'profile_image', 'password1', 'password2'] # Abstractuser에 다 있기 때문에 따로 선언하지 않아도 username과 같은 것으로 사용 가능하다.