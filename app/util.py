import inspect
from functools import wraps

import numpy as np
import pandas as pd
from django.shortcuts import render
from sklearn.metrics import roc_auc_score
from skpsl import ProbabilisticScoringList

from .models import Dataset, Subject


def psl_request(func=None, *, target="pslresult.pug"):
    def decorate(func):
        @wraps(func)
        def wrapper(request, subj_id):
            subj = Subject.objects.get(id=subj_id)
            pslparams = subj.last_model
            kwargs_full = dict(subj=subj, pslparams=pslparams, request=request)

            sig = inspect.signature(func)
            valid_params = set(sig.parameters.keys())
            filtered_kwargs = {key: value for key, value in kwargs_full.items() if key in valid_params}

            added_context = func(**filtered_kwargs)
            return render(
                request,
                target,
                fit_psl(subj.dataset, pslparams.features, pslparams.scores)
                | dict(historylength=subj.hist_len)
                | (added_context or dict()),
            )

        return wrapper

    if func is not None and callable(func):
        # arg contains only a function, we decorate it
        return decorate(func)
    else:
        return decorate


def fit_psl(dataset: Dataset, features=None, scores=None, k="predef"):
    # TODO use caching i.e. the PslResults table
    df = pd.read_csv(dataset.path)
    X = df.iloc[:, 1:]
    y = df.iloc[:, 0]
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
