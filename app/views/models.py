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


def save_model(request, subj_id):
    subj = Subject.objects.get(id=subj_id)
    name = request.POST.get("name")
    # check if there is already model with the same name
    if PslParam.objects.filter(name=name).exists():
        return render("Model with this name already exists", status=400)

    # i think we need to create two models here, the one that is needed for history and then one that is using currently
    PslParam.objects.create(**(dict(name=name) | subj.last_model.data))
    PslParam.objects.create(**(dict(name="current") | subj.last_model.data))

    historylength = subj.hist_len
    return render(request, "historybutton.pug", dict(historylength=historylength))