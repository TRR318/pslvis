from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.
import pandas as pd


def index(request):
    # Create a simple DataFrame
    data = {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "Job": ["Engineer", "Doctor", "Artist"],
    }
    df = pd.DataFrame(data)

    return render(request, "index.pug",  {'rows': df.itertuples(index=False)})


def update_table(request):
    print(request.GET)
    data = {
        "Namus": ["Alica", "Bobus", "Charlus"],
        "Agus": [25, 30, 35],
        "Jobus": ["Engineerus", "Doctorus", "Artistus"],
    }
    df = pd.DataFrame(data)
    
    return render(request, "table.pug", {'rows': df.itertuples(index=False)})
