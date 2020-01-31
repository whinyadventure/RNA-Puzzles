from django.http import HttpResponse
from guardian.decorators import permission_required

from rnapuzzles.models import PuzzleInfo, Challenge, ChallengeFile

import io
import zipfile


def file_download_batch(request, pk):

    challenge = Challenge.objects.get(pk=pk)
    files = challenge.challengefile_set.all()
    archive_name = 'puzzle_{}-{}_input_files.zip'.format(challenge.puzzle_info.pk, challenge.round)

    in_memory_zip = io.BytesIO()

    with zipfile.ZipFile(in_memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:

        for single in files:

            with single.file.open('rb') as f:
                single_content = f.read()

            zf.writestr(single.file.name, single_content)

    response = HttpResponse(in_memory_zip.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % archive_name

    return response


def file_download(request, pk):

    challenge_file = ChallengeFile.objects.get(pk=pk)
    file_content = open(challenge_file.file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % challenge_file.file.name

    return response


def pdb_download(request, pk):

    puzzle = PuzzleInfo.objects.get(pk=pk)
    file_content = open(puzzle.pdb_file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % puzzle.pdb_file.name

    return response