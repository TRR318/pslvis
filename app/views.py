from pathlib import Path
from django.shortcuts import render, redirect

from .models import *
from skpsl import ProbabilisticScoringList
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.metrics import roc_auc_score

from datetime import datetime


def create_subject(request, experiment):
    # create new subject
    subj = Subject.objects.create(
        experiment=Experiment.objects.get(sid=experiment),
    )

    # load index page
    return redirect(f"/{experiment}/{subj.id}/")


def index(request, experiment, subject):
    Subject.objects.get(id=subject)

    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    try:
        user_table = Subject.objects.get(session_key=session_key)
    except Data.DoesNotExist:
        user_table = Data(
            session_key=session_key, data_field=dict(features=[], scores={})
        )
        user_table.save()

    return render(
        request,
        "index.pug",
        fit_psl(user_table.features, user_table.scores) | dict(historylength=100),
    )


def update_table(request, experiment, subject):
    print(request.GET)

    session_key = request.session.session_key
    table = Data.objects.get(session_key=session_key)

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
            result = fit_psl(table.features, table.scores)
        case "score":
            feature_index = int(request.GET.get("feature"))
            diff = int(request.GET.get("diff"))
            table.update_score(feature_index, diff=diff)
            result = fit_psl(table.features, table.scores)
        case "reset":
            table.reset()
            result = fit_psl(table.features, table.scores)
        case "add":
            result = fit_psl(table.features, table.scores, k=len(table.features) + 1)
            table.insert_feature(result["features"][-1], None, result["scores"][-1])
        case "fill":
            result = fit_psl(table.features, table.scores, None)

            table.reset()
            for f, s in zip(result["features"], result["scores"]):
                table.insert_feature(f, None, s)

            result = fit_psl(table.features, table.scores)

    return render(request, "pslresult.pug", result | dict(historylength=100))


def updateHistory(request):
    # TODO
    histln = 2
    name = request.GET.get("saveName") or f"{histln} {datetime.now().isoformat()}"
    return render(request, "history.pug", None)


class Dataset:
    X, y, f = None, None, None

    def __call__(self):
        if Dataset.X is None:
            p = Path("data/schüler.csv")
            if p.is_file():
                df = pd.read_csv(p.absolute())
                target = "dropout"
                all_features = [
                    "age_enroll",
                    "migrant",
                    "Gesamtnote Abschlusszeugnis",
                    "Big Five: Gewissenhaftigkeit",
                    "Big Five: Verträglichkeit",
                    "Big Five: Extraversion",
                    "Big Five: Offenheit/Intellekt",
                    "Big Five: Neurotizismus",
                    "fernstudium",
                    "berufsbegleitendes Studium",
                    "study_Ing",
                    "study_ReWiSo",
                    "male",
                    "study_SprKult",
                    "study_Sport",
                    "study_MatNat",
                    "study_MedGesund",
                    "study_agrar",
                    "study_Kunst",
                ]
                #'gymnasium', 'mathe_leistungskurs','dualer Studiengang',
                Dataset.X, y = df[all_features], df[target]
                Dataset.y = np.array(y == 1, dtype=int)
                Dataset.f = all_features
            else:
                Dataset.X, y = fetch_openml(
                    data_id=42900, return_X_y=True, as_frame=False
                )
                Dataset.y = np.array(y == 2, dtype=int)
                Dataset.f = [
                    "Age (years)",
                    "BMI (kg/m2)",
                    "Glucose (mg/dL)",
                    "Insulin (microgram/mL)",
                    "HOMA",
                    "Leptin (ng/mL)",
                    "Adiponectin (microg/mL)",
                    "Resistin (ng/mL)",
                    "MCP-1 (pg/dL)",
                ]
        return Dataset.X, Dataset.y, Dataset.f


def fit_psl(features=None, scores=None, k="predef"):
    X, y, f = Dataset()()

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
