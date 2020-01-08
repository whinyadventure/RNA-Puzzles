from django import forms
from django.db.models import Q

from rnapuzzles.models import PuzzleInfo, Challenge


class SelectForm(forms.Form):
    choice = forms.ModelChoiceField(label='Choose base challenge', required=True,
                                    queryset=PuzzleInfo.objects
                                    .filter(id__in=Challenge.objects
                                            .filter(Q(id__in=Challenge.objects
                                                      .order_by('puzzle_info', '-round')
                                                      .distinct('puzzle_info'))
                                                    & Q(current_status=4))
                                            .values('puzzle_info_id')))

    # get last round of each puzzle_info and filter only completed
