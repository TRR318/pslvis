from django.shortcuts import render

from .models import Data
from skpsl import ProbabilisticScoringList
import numpy as np
from sklearn.datasets import fetch_openml


def index(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    try:
        user_table = Data.objects.get(session_key=session_key)
    except Data.DoesNotExist:
        user_table = Data(session_key=session_key, data_field=[])
        user_table.save()

    unused, headings, table = fit_psl(user_table.features)

    return render(request, "index.pug", dict(var=unused,headings=headings, rows=table))


def update_table(request):
    print(request.GET)
    from_ = int(request.GET.get("from")) - 1
    to_ = int(request.GET.get("to")) - 1
    feature = int(request.GET.get("feature"))
    fromlist = request.GET.get("fromList")
    tolist = request.GET.get("toList")

    session_key = request.session.session_key

    table = Data.objects.get(session_key=session_key)

    if fromlist == "unused" and tolist == "used":
        table.insert_feature(feature, to_)
    elif fromlist == "used" and tolist == "unused":
        table.remove_feature(feature)
    elif fromlist == tolist == "used":
        table.move_feature(from_, to_)

    unused, headings, table = fit_psl(table.features)

    return render(request, "table.pug", dict(var=unused, headings=headings, rows=table))


def fit_psl(features=None):
    X, y = fetch_openml(data_id=42900, return_X_y=True, as_frame=False)
    y = np.array(y == 2, dtype=int)

    psl = ProbabilisticScoringList({1})
    psl.fit(X, y, predef_features=features, k="predef")
    f = [
        "Age (years)",
        "BMI (kg/m2)",
        "Glucose (mg/dL)",
        "Insulin (microgram/mL)",
        "HOMA",
        "Leptin (ng/mL)",
        "Adiponectin (microg/mL)",
        "Resistin (ng/mL)",
        "MCP-1(pg/dL)",
    ]
    df = psl.inspect(feature_names=f)
    features = features or []
    unused = {i: v for i, v in enumerate(f) if i not in features}
    table = {
        i: [f"{e:.0%}" if k > 3 else e for k, e in enumerate(v)][2:]
        for i, v in zip(
            features, list(df.itertuples(index=False))[1:]
        )
    }
    return unused, list(df.columns[2:]), table
