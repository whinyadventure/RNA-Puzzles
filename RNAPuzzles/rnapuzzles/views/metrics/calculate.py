from django import forms
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse
from guardian.decorators import permission_required_or_403

from rnapuzzles.celery import spawn_tasks
from rnapuzzles.models import Submission, Challenge, PuzzleInfo


class FormSingle(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ["alignment"]

@permission_required_or_403('rnapuzzles.metrics_challenge',
        (Challenge, 'pk', 'pk'), accept_global_perms=True)
def calculate_metrics(request, pk):
    challenge = get_list_or_404(Challenge, pk=pk)[0]
    submissions = Submission.get_last_submissions(pk)
    FormSet = modelformset_factory(Submission, fields=["alignment"], extra=0)
    alignment = FormSingle(request.POST if request.method == "POST" else None, instance=challenge)
    res = FormSet(request.POST if request.method == "POST" else None, queryset=submissions, prefix='formset_input')
    for f in res:

        if f.instance.status == 1:
            alignment.fields["alignment"].disabled = True
            f.fields["alignment"].disabled = True
    if request.method == "POST":
        if res.is_valid() and alignment.is_valid():

            if "save" in request.POST:
                res.save(commit=True)
                alignment.save()
            if "metrics" in request.POST:
                alignment.save()

            post_keys = set(request.POST.keys())
            for s in res:
                if "single_%s" %s.instance.pk in post_keys or "metrics" in request.POST:
                    res.save()
                    if s.instance.status != 1:
                        spawn_tasks(s.instance.pk)
            return redirect(reverse('metrics-calculate', args=[pk]))


    return render(request, "test.html", {"res": res, "challenge": Challenge.objects.get(pk=pk), "alignment":alignment})