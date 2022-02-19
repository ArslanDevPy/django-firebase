from django.contrib import messages
from django.views.generic import TemplateView
from myapp.forms import UploaderForm
from django.http import HttpResponseRedirect
import pyrebase
from django.core.files.storage import default_storage, FileSystemStorage
from .firebase_config import firebaseConfig
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


class UploaderTemplateView(TemplateView):
    template_name = "myapp/uploader.html"

    def get_context_data(self, **kwargs):
        context = super(UploaderTemplateView, self).get_context_data(**kwargs)
        context['form'] = UploaderForm()
        context['path'] = self.request.path
        return context

    def post(self, request, *args, **kwargs):
        fm = UploaderForm(request.POST, request.FILES)
        if fm.is_valid():
            file = request.FILES['img']
            file_save = default_storage.save(file.name, file)
            storage.child("file/" + file_save).put("media/img/" + file_save)
            img_path = storage.child("file/" + file_save).get_url("")
            print(img_path)
            # delete = default_storage.delete(file.name)
            messages.success(request, "Data is Firebase Storage successful")
        return HttpResponseRedirect(str(request.path))
