from django.views.generic.edit import FormView

from ...models import CustomUser

class NewPassword(FormView):

    model = CustomUser