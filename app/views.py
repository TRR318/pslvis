from pathlib import Path
from django.shortcuts import render, redirect
from django.conf import settings

from .models import *
from skpsl import ProbabilisticScoringList
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from datetime import datetime


def create_subject(request, experiment):
    # create new subject
    subj = Subject.objects.create(
        experiment=Experiment.objects.get(id=experiment),
    )

    # load index page
    return redirect(f"{experiment}/{subj.id}/")


def index(request, experiment, subject):
    subj = Subject.objects.get(id=subject)
    model = subj.last_model

    return render(
        request,
        "index.pug",
        fit_psl(subj.dataset,model.features, model.scores) | dict(historylength=100) | dict(standalone = settings.STANDALONE),
    )


def update_table(request, experiment, subject):
    subj = Subject.objects.get(id=subject)
    table = subj.last_model
    match request.GET.get("type"):
        case "feature":
            feature_index = int(request.GET.get("feature"))
            fromlist = request.GET.get("fromList")
            tolist = request.GET.get("toList")

            if fromlist == "used" and tolist == "unused":
                table.remove_feature(feature_index)
            elif fromlist == "unused" and tolist == "used":
                to_ = request.GET.get("to", None)
                to_ = None if to_ is None else int(to_) - 1
                table.insert_feature(feature_index, to_)
            elif fromlist == tolist == "used":
                from_ = int(request.GET.get("from")) - 1
                to_ = int(request.GET.get("to")) - 1
                table.move_feature(from_, to_)
            result = fit_psl(subj.dataset,table.features, table.scores)
        case "score":
            feature_index = int(request.GET.get("feature"))
            diff = int(request.GET.get("diff"))
            table.update_score(feature_index, diff=diff)
            result = fit_psl(subj.dataset,table.features, table.scores)
    return render(request, "pslresult.pug", result | dict(historylength=100))


def reset(request, experiment, subject):
    table = Subject.objects.get(id=subject).last_model
    table.reset()
    return render(request, "pslresult.pug", fit_psl(subj.dataset,table.features, table.scores) | dict(historylength=100))

def add(request, experiment, subject):
    subj = Subject.objects.get(id=subject)
    table = subj.last_model    
    result = fit_psl(subj.dataset,table.features, table.scores, k=len(table.features) + 1)
    if len(table.features) < len(result["features"]):
        # only add a feature if we have not yet added all features
        table.insert_feature(result["features"][-1], None, result["scores"][-1])
    return render(request, "pslresult.pug", fit_psl(subj.dataset,table.features, table.scores) | dict(historylength=100))

def fill(request, experiment, subject):
    subj = Subject.objects.get(id=subject)
    table = subj.last_model
    result = fit_psl(subj.dataset, table.features, table.scores, None)
    table.reset()
    for f, s in zip(result["features"], result["scores"]):
        table.insert_feature(f, None, s)
    return render(request, "pslresult.pug", fit_psl(subj.dataset,table.features, table.scores) | dict(historylength=100))

def updateHistory(request):
    # TODO
    histln = 2
    name = request.GET.get("saveName") or f"{histln} {datetime.now().isoformat()}"
    return render(request, "history.pug", None)

def fit_psl(dataset:Dataset, features=None, scores=None, k="predef"):
    # TODO use caching i.e. the PslResults table

    # TODO properly get the dataset from the database
    df = pd.read_csv(dataset.path)
    X = df.iloc[:,:1]
    y = df.iloc[:,0]
    f = dataset.featurenames


    psl = ProbabilisticScoringList({-1, 1, 2})
    scores = [scores[f_] for f_ in features]
    psl.fit(X, y, predef_features=features, predef_scores=scores, k=k)
    df = psl.inspect(feature_names=f)

    features = features or []
    unused = {i: v for i, v in enumerate(f) if i not in features}

    if "Feature" not in df:
        df["Feature"] = np.nan
    if "Threshold" not in df:
        df["Threshold"] = np.nan

    table = pd.DataFrame(
        dict(
            # calculate feature index
            fidx=psl.inspect()["Feature Index"].map(
                lambda v: "" if np.isnan(v) else f"{v:.0f}"
            ),
            fname=df["Feature"].fillna(""),
            # remove last two digits of the 4 decimal places in thre threshold
            thresh=df["Threshold"].fillna("").map(lambda v: v[:-2]),
            # convert score to integer
            score=df["Score"].map(lambda v: "" if np.isnan(v) else f"{v:.0f}"),
            probas=pd.Series(
                df[[col for col in df.columns if col.startswith("T = ")]]
                .map(lambda v: "" if np.isnan(v) else f"{v:.0%}")
                .agg(list, axis=1),
                name="Probas",
            ),
        )
    ).to_dict("records")[
        1:
    ]  # drop stage 0 and convert into list of dicts

    return dict(
        var=unused,
        headings=[col[4:] for col in df.columns if col.startswith("T = ")],
        rows=table,
        labels=list(range(len(psl))),
        metric=[roc_auc_score(y, stage.predict_proba(X)[:, 1]) for stage in psl],
        features=psl.features,
        scores=psl.scores,
    )
