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

    return render(request, "index.pug", fit_psl(user_table.features))


def update_table(request):
    print(request.GET)

    session_key = request.session.session_key
    table = Data.objects.get(session_key=session_key)


    feature = int(request.GET.get("feature"))
    match request.GET.get("type"):
        case "feature":
            from_ = int(request.GET.get("from")) - 1
            to_ = int(request.GET.get("to")) - 1
            fromlist = request.GET.get("fromList")
            tolist = request.GET.get("toList")

            if fromlist == "unused" and tolist == "used":
                table.insert_feature(feature, to_)
            elif fromlist == "used" and tolist == "unused":
                table.remove_feature(feature)
            elif fromlist == tolist == "used":
                table.move_feature(from_, to_)
        case "score":
            score = int(request.GET.get("score"))


    return render(request, "pslresult.pug", fit_psl(table.features))


class Dataset:
    X, y = None, None

    def __call__(self):
        if self.X is None:
            self.X, y = fetch_openml(data_id=42900, return_X_y=True, as_frame=False)
            self.y = np.array(y == 2, dtype=int)
        return self.X, self.y


def fit_psl(features=None):
    X, y = Dataset()()

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
        "MCP-1 (pg/dL)",
    ]
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
    labels, data = list(zip(*enumerate((stage.score(X, y) for stage in psl))))
    labels = list(labels)
    data = list(data)
    return dict(
        var=unused, headings=list(df.columns[2:]), rows=table, labels=labels, data=data
    )
