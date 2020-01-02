from django.views.generic.edit import FormView
from django.contrib.auth import logout

from .signinForm import SiginForm

class Signin(FormView):
    template_name = "registration/login.html"
    success_url = "/"
    form_class = SiginForm

    def get_initial(self):
        self.initial.update({'request': self.request})
        return self.initial

    def logout(request):
        logout(request)