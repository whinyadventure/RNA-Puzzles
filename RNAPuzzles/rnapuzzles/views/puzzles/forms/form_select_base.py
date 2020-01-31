from django.utils import timezone
from django import forms
from django.db.models import Q

from rnapuzzles.models import PuzzleInfo, Challenge


class SelectForm(forms.Form):

    choice = forms.ModelChoiceField(label='Choose base challenge', required=True, queryset=PuzzleInfo.objects.none())

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(SelectForm, self).__init__(*args, **kwargs)

        self.fields['choice'].queryset = PuzzleInfo.objects\
            .filter(id__in=Challenge.objects
                    .filter(Q(id__in=Challenge.objects
                              .order_by('puzzle_info', '-round')
                              .distinct('puzzle_info'))
                            & Q(result_published=True)
                            & Q(author=current_user))
                    .values('puzzle_info_id'))
