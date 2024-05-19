from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect

from app.util import fit_psl, psl_request
from .models import *


def create_subject(request, ex_id):
    # create new subject
    subj = Subject.objects.create(
        experiment=Experiment.objects.get(id=ex_id),
    )

    # load index page
    return redirect(f"{subj.id}/")


@psl_request(target="index.pug")
def index(subj: Subject):
    return dict(standalone=settings.STANDALONE, model_names=[model.name for model in subj.models.iterator()])


@psl_request
def update_table(pslparams, request):
    match request.POST.get("type"):
        case "feature":
            feature_index = int(request.POST.get("feature"))
            fromlist = request.POST.get("fromList")
            tolist = request.POST.get("toList")

            if fromlist == "used" and tolist == "unused":
                pslparams.remove_feature(feature_index)
            elif fromlist == "unused" and tolist == "used":
                to_ = request.POST.get("to", None)
                to_ = None if to_ is None else int(to_) - 1
                pslparams.insert_feature(feature_index, to_)
            elif fromlist == tolist == "used":
                from_ = int(request.POST.get("from")) - 1
                to_ = int(request.POST.get("to")) - 1
                pslparams.move_feature(from_, to_)
        case "score":
            feature_index = int(request.POST.get("feature"))
            diff = int(request.POST.get("diff"))
            pslparams.update_score(feature_index, diff=diff)


@psl_request
def reset(pslparams):
    pslparams.reset()


@psl_request
def add(subj, pslparams):
    result = fit_psl(subj.dataset, pslparams.features, pslparams.scores, k=len(pslparams.features) + 1)
    if len(pslparams.features) < len(result["features"]):
        # only add a feature if we have not yet added all features
        pslparams.insert_feature(result["features"][-1], None, result["scores"][-1])


@psl_request
def fill(subj, pslparams):
    result = fit_psl(subj.dataset, pslparams.features, pslparams.scores, None)
    pslparams.reset()
    for f, s in zip(result["features"], result["scores"]):
        pslparams.insert_feature(f, None, s)


def updateHistory(request, subj_id):
    subj = Subject.objects.get(id=subj_id)
    name = request.POST.get("saveName") or f"{subj.hist_len} {datetime.now().isoformat()}"

    # TODO copy model

    return render(request, "history.pug", dict(model_names=[model.name for model in subj.models.iterator()]))
