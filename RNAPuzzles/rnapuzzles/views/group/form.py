from django import forms

from ...models import Group, CustomUser


class Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = kwargs['initial']['request']
        user = CustomUser.objects.get(id=self.request.user.id)
        group = Group.objects.get(group_name=kwargs['instance'])
        if not user.has_perm("edit_group_name", group):
            self.fields["group_name"].widget = forms.HiddenInput()

    class Meta:
        model = Group
        fields = ["group_name", "group_description"]
