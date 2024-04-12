from django.shortcuts import render

from .models import Data

INITIAL_TABLE_DATA = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Job": ["Engineer", "Doctor", "Artist"],
}


def index(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    try:
        user_table = Data.objects.get(session_key=session_key)
    except Data.DoesNotExist:
        user_table = Data(session_key=session_key, data_field=INITIAL_TABLE_DATA)
        user_table.save()

    return render(request, "index.pug", {"rows": user_table.data})


def update_table(request):
    print(request.GET)
    from_ = int(request.GET.get("from")) - 1
    to_ = int(request.GET.get("to")) - 1

    session_key = request.session.session_key

    user_table = Data.objects.get(session_key=session_key)
    df = user_table.df
    df.iloc[from_], df.iloc[to_] = df.iloc[to_].copy(), df.iloc[from_].copy()
    user_table.df = df
    return render(request, "table.pug", {"rows": list(df.itertuples(index=False))})
