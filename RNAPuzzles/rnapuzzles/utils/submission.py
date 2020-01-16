import datetime
import zipfile

from django.db.models import Q
from django.forms import forms

from rnapuzzles.models import PuzzleInfo, Submission

batch_file_formats = ["zip"]
file_file_formats = ["pdb", "cif", "in"]  # TODO


def is_batch(file_name):
    format = file_name.split(".")[-1]
    return format.lower() in batch_file_formats


def get_puzzle_id(name):
    return int(' '.join(name.split(".")[:-1]))


def get_file_format(name):
    return name.split(".")[-1]


def get_open_challenge(puzzle_info: PuzzleInfo):
    now = datetime.datetime.today()
    res = puzzle_info.challenge_set.all().filter(Q(start_date__lte=now) & Q(end_date__gte=now))
    if res.count() == 0:
        return None
    return res[0]  # TODO 2 open challenges


def validate_single(filename, content, pk=None):
    if pk is None:
        format = get_file_format(filename)
        if format not in file_file_formats:
            raise forms.ValidationError(
                "file %s: Wrong file format. Accepted file formats: %s" % (str(filename),
                                                                                         ",".join(
                                                                                             file_file_formats)))
        try:
            pk = get_puzzle_id(filename)
        except:
            # TODO
            forms.ValidationError(
                "%s: Wrong file name." % (filename)
            )
    puzzle_info: PuzzleInfo = PuzzleInfo.objects.filter(pk=pk)
    if puzzle_info.count() == 0:
        raise forms.ValidationError("File %s: Could't find Puzzle with id equal to %s" % (filename, str(pk)))
    puzzle_info = puzzle_info[0]
    if get_open_challenge(puzzle_info) is None:
        raise forms.ValidationError("File %s: Could't find open challenge for puzzle %s" % (filename, str(pk)))

    try:
        content.decode("utf-8")
    except:
        raise forms.ValidationError("File %s: Could't decode file content to utf-8" % (filename))


def validate_batch(file):
    erros = []
    myzipfile = zipfile.ZipFile(file)
    for name in myzipfile.filelist:
        content = myzipfile.read(name)
        filename = name.filename
        try:
            validate_single(filename, content)
        except forms.ValidationError as err:
            erros.append(err.message)
    if (len(erros)):
        raise forms.ValidationError(erros)


def save_single(name, content, user, puzzle_pk=None):
    try:
        content = content.decode("utf-8")
    except:
        pass

    if puzzle_pk is None:
        puzzle_info = PuzzleInfo.objects.get(pk=get_puzzle_id(name))
    else:
        puzzle_info = PuzzleInfo.objects.get(pk=puzzle_pk)

    challenge = get_open_challenge(puzzle_info)
    return Submission.objects.create(challenge_id=challenge.pk, user=user, content=content)


def save_zip(file, user):
    myzipfile = zipfile.ZipFile(file)
    res = []
    for name in myzipfile.filelist:
        content = myzipfile.read(name)
        filename = name.filename
        res.append(save_single(filename, content, user))
    return res
