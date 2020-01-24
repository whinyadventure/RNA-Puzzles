import datetime
import zipfile

from django.db.models import Q
from django.forms import forms

from rnapuzzles.models import PuzzleInfo, Submission, Challenge
import re

batch_file_formats = ["zip"]
single_file_formats = ["pdb"]  # TODO
max_label_length = 10

def get_file_format(name):
    return name.split(".")[-1].lower()


def is_batch(file_name):
    return get_file_format(file_name) in batch_file_formats


def get_puzzle_info(name):
    res = re.findall("^(\d+)(_.+)?.pdb$", name)
    return {"pk":int(res[0][0]), "label":res[0][1]}


def get_puzzle_pk(name, pk):
    if pk:
        return pk
    res: str = get_puzzle_info(name)["pk"]
    if res.isdecimal():
        return int(res)
    return None


def get_puzzle_label(name, label):
    if label:
        return label
    res: str = get_puzzle_info(name)["label"]
    if res != "":
        return res
    return None


def get_open_challenge(puzzle_info: PuzzleInfo):
    now = datetime.datetime.today()
    res = puzzle_info.challenge_set.all().filter(Q(start_date__lte=now) & Q(end_date__gte=now))
    if res.count() == 0:
        return None
    return res[0]  # TODO 2 open challenges


def validate_single(filename, content, pk: str, label: str):
    if not get_file_format(filename) in single_file_formats:
        raise forms.ValidationError("File %s: Wrong file format" % (filename))

    if label is None or label == "":
        raise forms.ValidationError("File %s: Label was not provided" % (filename))

    if not pk.isdecimal():
        raise forms.ValidationError("File %s: Wrong name format, should be <puzzle number>_<label>.pdb %s" % (filename))

    puzzle_info: PuzzleInfo = PuzzleInfo.objects.filter(pk=int(pk))
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
        pk, label = get_puzzle_info(name.filename)

        try:
            validate_single(filename, content, pk, label)
        except forms.ValidationError as err:
            erros.append(err.message)
    if (len(erros)):
        raise forms.ValidationError(erros)


def save_single(content, user, puzzle_pk, label):
    print(content)
    content = content.decode("utf-8")
    puzzle_info = PuzzleInfo.objects.get(pk=puzzle_pk)

    challenge: Challenge = get_open_challenge(puzzle_info)
    is_automatic = challenge.end_automatic > datetime.datetime.now()
    return Submission.objects.create(challenge_id=challenge.pk, user=user, content=content, is_automatic=is_automatic, label=label)


def save_batch(file, user):
    myzipfile = zipfile.ZipFile(file)
    res = []
    for name in myzipfile.filelist:
        content = myzipfile.read(name)
        pk, label = get_puzzle_info(name.filename)
        res.append(save_single(content, user, pk, label))
    return res
