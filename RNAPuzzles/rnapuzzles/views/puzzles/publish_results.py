from django.shortcuts import redirect
from django.urls import reverse
from guardian.decorators import permission_required

from rnapuzzles.models import Challenge


def publish_results(request, pk):

    challenge = Challenge.objects.get(pk=pk)
    challenge.result_published = True
    challenge.save()

    return redirect(reverse('show-results', kwargs={'pk': pk}))
