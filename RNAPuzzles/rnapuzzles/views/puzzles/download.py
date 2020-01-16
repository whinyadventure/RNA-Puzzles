from django.http import HttpResponse
from guardian.decorators import permission_required

from rnapuzzles.models import PuzzleInfo, ChallengeFile

@permission_required("rnapuzzles.view_puzzleinfo")
def file_download(request, pk):

    challenge_file = ChallengeFile.objects.get(pk=pk)
    file_content = open(challenge_file.file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % challenge_file.file.name

    return response

@permission_required("rnapuzzles.view_puzzleinfo")
def pdb_download(request, pk):

    puzzle = PuzzleInfo.objects.get(pk=pk)
    file_content = open(puzzle.pdb_file.path, 'rb')
    response = HttpResponse(file_content, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename=%s" % puzzle.pdb_file.name

    return response