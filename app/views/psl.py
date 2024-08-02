import inspect
from functools import wraps
from html import escape

import numpy as np
from django.shortcuts import render

from app.models import Subject, PslParam
from app.util import fit_psl
from pslvis import settings


def psl_request(func=None, *, target="pslresult.pug"):
    def decorate(func):
        @wraps(func)
        def wrapper(request, subj_id, **kwargs):
            subj = Subject.objects.get(id=subj_id)

            model_id = kwargs.get("model_id") or request.POST.get("modelID")
            if model_id is None:
                pslparams = subj.last_model
            else:
                pslparams = PslParam.objects.get(id=model_id)

            kwargs_full = dict(subj=subj, pslparams=pslparams, request=request)

            sig = inspect.signature(func)
            valid_params = set(sig.parameters.keys())
            filtered_kwargs = {key: value for key, value in kwargs_full.items() if key in valid_params}

            added_context = func(**filtered_kwargs)
            psl = fit_psl(subj.dataset, pslparams.features, pslparams.scores)

            return render(
                request,
                target,
                psl
                | dict(historylength=subj.hist_len)
                | compute_tree(psl)
                | (added_context or dict())
                | dict(experiment_params=subj.experiment.params)
            )

        return wrapper

    if func is not None and callable(func):
        # arg contains only a function, we decorate it
        return decorate(func)
    else:
        return decorate


@psl_request(target="index.pug")
def index(subj: Subject):
    return dict(standalone=settings.STANDALONE, models=subj.model_dict)


@psl_request(target="model_as_table.pug")
def get():
    pass


@psl_request(target="model_as_tree.pug")
def gettree():
    pass


def compute_tree(psl):
    names = [row["fname"] + row["thresh"] for row in psl["rows"]]
    if not names:
        return dict(merm_chart_proba="flowchart TD", merm_chart="flowchart TD")
    scores = np.array(psl["scores"])
    probas = {int(h): p for h, p in zip(psl["headings"], psl["rows"][-1]["probas"])}

    results = dict()
    for with_proba in [True, False]:
        output = ["""---
    config:
      theme: base
      themeVariables:
        primaryColor: "#fff"\n---""", "flowchart TD", "\t0(0)"]

        for i, (name, score) in enumerate(zip(names, scores)):
            for k, j in enumerate(range(2 ** i - 1, 2 ** (i + 1) - 1)):
                for m in range(2):
                    binary_str = f"{k * 2 + m:0{i + 1}b}" + "0" * (len(scores) - i - 1)
                    s = np.array([int(x) for x in binary_str]) @ scores
                    p = f"<br/>{probas[s]}" if with_proba and i == len(scores) - 1 else ""
                    label = f'|"{escape(name)}"| ' if m == 1 else ""
                    output.append(f'\t{j} --> {label}{j * 2 + m + 1}("{s}{p}")')
        results["merm_chart" + ("_proba" if with_proba else "")] = "\n".join(output)

    return results


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
