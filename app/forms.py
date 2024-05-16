from django import forms
from django.core.exceptions import ValidationError
from .models import Dataset

import pandas as pd

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = '__all__'

    def clean_featurenames(self):
        features = self.cleaned_data.get('featurenames')
        n_features = len(pd.read_csv(self.files.get("filepath",self.initial.get("filepath")).file, nrows=0).columns) -1
                
        if len(features) != n_features:
            raise ValidationError(f"The featurenames list (len={len(features)}) must be one shorter than the column count ({n_features}) of the csv. Note that the first column is interpret as the target variable.")
        return features

    def clean_filepath(self):
        try:
            filepath = self.cleaned_data.get("filepath")
            file = filepath.file
            file.seek(0)
            df = pd.read_csv(file)
            if not set(df.iloc[:,0]) <= {0,1}:
                raise ValidationError("Column one must be the target column and only contain 0 and 1 values")
            return filepath
        except pd.EmptyDataError:
            raise ValidationError("Dataset apears to be empty")
        except Exception:            
            raise ValidationError("Appears not to be a csv")
        
        