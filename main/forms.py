from django import forms

class RegisterForm(forms.Form):
    f_name = forms.CharField(label='First Name',min_length=2, max_length=100)
    l_name = forms.CharField(label='Last Name',min_length=2, max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    pw_hash = forms.CharField(label='Password',min_length=2, max_length=250, widget=forms.PasswordInput)
    confirm_pw = forms.CharField(label='Confirm Password',min_length=2, max_length=250, widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    pw_hash = forms.CharField(label='Password',min_length=2, max_length=250, widget=forms.PasswordInput)