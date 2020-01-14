from django import forms
from martor.fields import MartorFormField
from django.utils.translation import ugettext_lazy as _


from ...models import Group, CustomUser


class Form(forms.ModelForm):

    group_description = MartorFormField()

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        user = CustomUser.objects.get(id=self.request.user.id)
        group = Group.objects.get(group_name=kwargs['instance'])

        if not user.has_perm("name_group", group):
            self.fields["group_name"].widget = forms.HiddenInput()
            self.fields["contact"].widget = forms.HiddenInput()

    class Meta:
        model = Group
        fields = ["group_name", "contact", "group_description"]
