from django.views.generic.edit import FormView
from django.contrib.auth import logout

from .signinForm import SigninForm


class Signin(FormView):

    template_name = "registration/login.html"
    success_url = "/"
    form_class = SigninForm

    def get_initial(self):
        self.initial.update({'request': self.request})

        return self.initial

    def logout(request):
        logout(request)
