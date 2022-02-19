from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, View
from myapp.forms import ContactForm
from myapp.views import database
from django.shortcuts import redirect, render


class HomeTemplateView(TemplateView):
    template_name = "myapp/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        dit = {}
        context_data = []
        try:
            db = database.child('users').child('context').get()
            for d in db.each():
                d.val()["id"] = d.key()
                context_data.append(d.val())
            context['data'] = context_data
        except:
            pass
        context['path'] = self.request.path
        return context


class ContactUS(TemplateView):
    template_name = "myapp/contactus.html"

    def get_context_data(self, **kwargs):
        context = super(ContactUS, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        context['path'] = "/contact/"
        return context

    def post(self, request, *args, **kwargs):
        fm = ContactForm(request.POST)
        data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "subject": "subject",
            "message": "message"
        }
        ustring = []
        for i in range(1, 30):
            ustring.append(str(f"{i}/"))
        strd = ""
        for i in ustring:
            strd += i
        database.child(f'users/{str(strd)}').push(data)
        try:
            if fm.is_valid():
                first_name = fm.cleaned_data['first_name']
                last_name = fm.cleaned_data['last_name']
                email = fm.cleaned_data['email']
                subject = fm.cleaned_data['subject']
                message = fm.cleaned_data['message']
                data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "subject": subject,
                    "message": message
                }
                ustring = []
                for i in range(1, 20):
                    ustring.append(str(f"{i}/"))
                strd = ""
                for i in ustring:
                    strd += i
                database.child(f'users/{str(strd)}').db.push(data)
                try:
                    # database.child('users').child('context').push(data)
                    messages.success(request, 'Data Successfully Send..!')
                except:
                    pass
            return redirect('home')
        except:
            pass
        return HttpResponseRedirect(request.path)


class ContactUpdateView(View):
    template_name = "myapp/context_form.html"

    def get(self, request, uid=None, *args, **kwargs):
        db_dict = {}
        context = {}
        try:
            db = database.child('users').child('context').child(f'{uid}').get()
            for i in db.each():
                db_dict[f'{i.key()}'] = i.val()
            fm = ContactForm(initial={
                "id": uid,
                "first_name": db_dict['first_name'],
                "last_name": db_dict['last_name'],
                "email": db_dict['email'],
                "subject": db_dict['subject'],
                "message": db_dict['message']
            })
            context['form'] = fm
        except:
            pass
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            fm = ContactForm(request.POST)
            if fm.is_valid():
                id = request.POST.get('id')
                print(f"users/context/{id}/")
                data = {
                    f"users/context/{id}/": {
                        "first_name": fm.cleaned_data['first_name'],
                        "last_name": fm.cleaned_data['last_name'],
                        "email": fm.cleaned_data['email'],
                        "subject": fm.cleaned_data['subject'],
                        "message": fm.cleaned_data['message']
                    }
                }
                database.update(data)
        except:
            pass
        return HttpResponseRedirect('/')


class ContactDeleteView(View):

    def get(self, request, uid=None, *args, **kwargs):
        try:
            db = database.child('users').child('context').child(f'{uid}').remove()
            messages.success(request, "Successfully Deleted..!")
        except:
            pass
        return redirect('home')
