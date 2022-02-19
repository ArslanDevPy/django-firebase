from django.core.files.storage import default_storage
import pyrebase
from myapp.forms import LoginForm, SignupForm, ResetPasswordForm
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages
from .firebase_config import firebaseConfig


firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
auth = firebase.auth()
database = firebase.database()


class LoginTemplateView(TemplateView):
    template_name = "myapp/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginTemplateView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        context['path'] = self.request.path

        return context

    def post(self, request, *args, **kwargs):
        fm = LoginForm(request.POST)

        if fm.is_valid():
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                info = auth.get_account_info(user['idToken'])
                if info["users"][0]['emailVerified']:
                    request.session['token'] = user['idToken']
                    return HttpResponseRedirect('/')
                else:
                    messages.warning(request, 'This email is Not verified..!')
            except:
                pass
        return redirect("login")


class SignupTemplateView(TemplateView):
    template_name = "myapp/signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignupTemplateView, self).get_context_data(**kwargs)
        context['form'] = SignupForm()
        context['path'] = self.request.path
        return context

    def post(self, request, *args, **kwargs):
        fm = SignupForm(request.POST, request.FILES)
        if fm.is_valid():
            name = fm.cleaned_data['name']
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            confirm_password = fm.cleaned_data['confirm_password']
            image = request.FILES['image']
            if password == confirm_password:
                try:
                    pass
                    image_save = default_storage.save(image.name, image)
                    storage.child("users/" + image_save).put("media/img/" + image_save)
                    img_path = storage.child("users/" + image_save).get_url("")
                    user = auth.create_user_with_email_and_password(email, password)
                    auth.send_email_verification(user['idToken'])
                    if user:
                        localId = user['localId']
                        data = {"name": name, "status": "1", "image": img_path}
                        database.child("users").child(localId).child('details').set(data)
                        messages.success(request, "User Created Successfully..!")
                        return redirect("login")
                except:
                    pass
            else:
                messages.warning(request, "Password Not Mach Plz Try Again")
                return redirect("signup")
        else:
            context = {'error': fm.errors, 'form': SignupForm()}
            return render(request, self.template_name, context)
        return redirect("signup")


class PasswordResetTemplateView(TemplateView):
    template_name = "myapp/resetpassword.html"

    def get_context_data(self, **kwargs):
        context = super(PasswordResetTemplateView, self).get_context_data(**kwargs)
        context['form'] = ResetPasswordForm()
        return context

    def post(self, request, *args, **kwargs):
        fm = ResetPasswordForm(request.POST)
        if fm.is_valid():
            email = fm.cleaned_data['email']
            response = auth.send_password_reset_email(email)
            print(response)
        return redirect('home')


def userLogout(request):
    logout(request)
    return redirect("login")
