from pathlib import Path
from django.shortcuts import render

from .models import Data
from skpsl import ProbabilisticScoringList
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.metrics import balanced_accuracy_score


def index(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    try:
        user_table = Data.objects.get(session_key=session_key)
    except Data.DoesNotExist:
        user_table = Data(session_key=session_key, data_field=dict(features=[], scores={}))
        user_table.save()

    return render(request, "index.pug", fit_psl(user_table.features, user_table.scores))


def update_table(request):
    print(request.GET)

    session_key = request.session.session_key
    table = Data.objects.get(session_key=session_key)
    psl_length= "predef"

    match request.GET.get("type"):
        case "feature":
            feature_index = int(request.GET.get("feature"))
            fromlist = request.GET.get("fromList")
            tolist = request.GET.get("toList")

            if fromlist == "used" and tolist == "unused":
                table.remove_feature(feature_index)
            elif fromlist == "unused" and tolist == "used":
                to_ = int(request.GET.get("to")) - 1
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
        case "fill":
            result = fit_psl(table.features, table.scores, None)
            
            table.reset()
            for f,s in zip(result["features"], result["scores"]):
                table.insert_feature(f,None,s)
            
            result = fit_psl(table.features, table.scores)


    return render(request, "pslresult.pug", result)


class Dataset:
    X, y, f = None, None, None

    def __call__(self):
        if Dataset.X is None:
            p = Path("data/schüler.csv")
            if p.is_file():
                df = pd.read_csv(p.absolute())
                target = 'dropout'
                all_features = ['age_enroll', 'migrant','Gesamtnote Abschlusszeugnis', 'Big Five: Gewissenhaftigkeit', 'Big Five: Verträglichkeit',
                    'Big Five: Extraversion', 'Big Five: Offenheit/Intellekt',
                    'Big Five: Neurotizismus',                    'fernstudium',
                    'berufsbegleitendes Studium','study_Ing', 'study_ReWiSo',
                     'male',                     'study_SprKult',                    'study_Sport',  'study_MatNat', 'study_MedGesund',                    'study_agrar', 'study_Kunst']
                #'gymnasium', 'mathe_leistungskurs','dualer Studiengang',
                Dataset.X,y = df[all_features],df[target]
                Dataset.y = np.array(y == 1, dtype=int)
                Dataset.f = all_features
            else:
                Dataset.X, y = fetch_openml(data_id=42900, return_X_y=True, as_frame=False)
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

    psl = ProbabilisticScoringList({1})
    scores = [scores[f_] for f_ in features]
    psl.fit(X, y, predef_features=features, predef_scores=scores, k=k)
    df = psl.inspect(feature_names=f)
    features = features or []
    unused = {i: v for i, v in enumerate(f) if i not in features}

    def substitute(idx, v):
        if idx == 0:
            return v
        elif idx == 1:  # score
            return f"{v:.0f}"
        elif np.isnan(v):
            return ""
        else:
            return f"{v:.0%}"

    table = {
        row_idx: [substitute(k, e) for k, e in enumerate(v[2:])]
        for row_idx, v in zip(features, list(df.itertuples(index=False))[1:])
    }
    labels, data = list(zip(*enumerate((balanced_accuracy_score(y, stage.predict(X), adjusted=True) for stage in psl))))
    labels = list(labels)
    data = list(data)
    headings =list(df.columns[2:4]) +[s[4:] for s in df.columns[4:]]
    return dict(
        var=unused, headings=headings, rows=table, labels=labels, data=data, features=psl.features, scores=psl.scores
    )
