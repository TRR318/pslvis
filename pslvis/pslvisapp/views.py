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

    # Convert DataFrame to HTML
    html = df.to_html(index=False, table_id="data-table", classes=["table", "table-hover"])

    # Pass the HTML to the template
    context = {"loaded_data": html}
    return render(request, "index.pug", context)


def update_table(request):
    print(request.GET)
    data = {
        "Namus": ["Alica", "Bobus", "Charlus"],
        "Agus": [25, 30, 35],
        "Jobus": ["Engineerus", "Doctorus", "Artistus"],
    }
    df = pd.DataFrame(data)

    # Convert DataFrame to HTML
    html = df.to_html(index=False, table_id="data-table", classes=["table", "table-hover"])

    return HttpResponse(html)
