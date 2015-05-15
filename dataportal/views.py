import pprint
from django.shortcuts import render
from django.template import RequestContext
from dataportal import models


def index(request):
    return render(request, 'index.html',
                  {'data': True, 'msg': 'msg'},
                  context_instance=RequestContext(request))


def dc_info(request):

    dc_models = models.DcInfo.objects.all()

    dcs = []

    for dc_model in dc_models:
        dcs.append({
            'title': dc_model.title,
            'identifier': dc_model.identifier
        })

    return render(request, 'dc_info.html',
                  {'data': True,
                   'msg': 'msg',
                   'dcs': dcs},
                  context_instance=RequestContext(request))


def survey_metadata(request, wiserd_id):

    survey_link = models.QuestionLink

    print wiserd_id

    survey_models = models.Survey.objects.all()

    survey_data = []

    return render(request, 'dc_info.html',
                  {'data': True,
                   'msg': 'msg',
                   'survey_data': survey_data},
                  context_instance=RequestContext(request))