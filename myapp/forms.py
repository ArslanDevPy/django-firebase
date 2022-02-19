from django import forms
from myapp.validate import validate_image_extension, file_size


class UserForm(forms.Form):
    name = forms.CharField(max_length=50)
    father = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)


class LoginForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'type': 'password'}))


class SignupForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'type': 'password'}))
    confirm_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'type': 'password'}))
    image = forms.ImageField(validators=[validate_image_extension, file_size], help_text='Maximum file size allowed is '
                                                                                         '500kb', )


class UploaderForm(forms.Form):
    name = forms.CharField(max_length=50)
    img = forms.ImageField(validators=[validate_image_extension, file_size], help_text='Maximum file size allowed is '
                                                                                       '500kb', )


class ContactForm(forms.Form):
    id = forms.CharField(max_length=100, required=False,
                         widget=forms.TextInput(attrs={'type': 'hidden'}))
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
