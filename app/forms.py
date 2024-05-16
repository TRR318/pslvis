from django import forms
from django.core.exceptions import ValidationError
from .models import Dataset

# TODO check featurenames length with dataset
class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = '__all__'

    def clean_featurenames(self):
        features = self.cleaned_data.get('featurenames')
        # if len(features) > 10:
        #     raise ValidationError("The name must be at least 10 characters long.")
        return features
