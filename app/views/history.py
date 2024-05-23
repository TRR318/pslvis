from datetime import datetime

from django.shortcuts import render

from app.models import Subject, PslParam


def save_model(request, subj_id):
    subj = Subject.objects.get(id=subj_id)
    current = subj.last_model
    name = request.POST.get("savename") or f"{subj.hist_len} {datetime.now().isoformat()}"

    # create now entry thats a copy of the current
    PslParam.objects.create(**(dict(name=name) | subj.last_model.data)).save()
    # make sure, the current model stays the most recently added one
    current.save()

    return render(request, "history.pug", dict(models=subj.model_dict))
