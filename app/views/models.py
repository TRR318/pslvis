from datetime import datetime

from django.shortcuts import render
from django.views import View

from app.models import Subject, PslParam
from app.views.psl import psl_request


class ModelHandler(View):

    @staticmethod
    @psl_request
    def get():
        pass

    @staticmethod
    def put(request, subj_id, model_id):
        # duplicate Model
        subj = Subject.objects.get(id=subj_id)
        model = PslParam.objects.get(id=model_id)
        name = f"{model.name} Copy {datetime.now().isoformat()}"

        # create now entry thats a copy of the current
        PslParam.objects.create(**(dict(name=name) | subj.last_model.data)).save()

        return render(request, "models.pug", dict(models=subj.model_dict))

    def patch(self, request, subj_id, model_id):
        # rename model
        pass

    @staticmethod
    def delete(request, subj_id, model_id):
        # remove model
        PslParam.objects.get(id=model_id).hide()
        subj = Subject.objects.get(id=subj_id)
        return render(request, "models.pug", dict(models=subj.model_dict))
