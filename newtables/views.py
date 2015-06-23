import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from newtables import models


def newdb(request):
    a = models.NewSurvey.objects.using('new').all().values('surveyid')


    api_data = {'hi': 'ok',
                'a': a
                }
    return HttpResponse(json.dumps(api_data, indent=4), content_type="application/json")
