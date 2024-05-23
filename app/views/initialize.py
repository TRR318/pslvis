from django.shortcuts import redirect

from ..models import *


def create_subject(request, ex_id):
    # create new subject
    subj = Subject.objects.create(
        experiment=Experiment.objects.get(id=ex_id),
    )

    # load index page
    return redirect(f"{subj.id}/")
