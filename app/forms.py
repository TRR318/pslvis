from django import forms
from django.core.exceptions import ValidationError
from .models import Dataset

import pandas as pd
        
class DatasetForm(forms.ModelForm):
    filecontent = forms.FileField(label="Dataset as CSV. First column must be target")

    class Meta:
        model = Dataset
        fields = '__all__'

    def clean_filecontent(self):
        try:
            file = self.files.get("filecontent")
            df = pd.read_csv(file)
            if not set(df.iloc[:, 0]) <= {0, 1}:
                raise ValidationError("Column one must be the target column and only contain 0 and 1 values")

            file.seek(0)
            json_content = df.to_dict(orient='split')
            return json_content
        except pd.errors.EmptyDataError:
            raise ValidationError("Dataset appears to be empty")
        except Exception:
            raise ValidationError("Appears not to be a CSV")