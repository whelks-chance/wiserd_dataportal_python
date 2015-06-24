import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from newtables import models


def newdb(request):
    b = models.Survey.objects.using('new').all().values('surveyid')

    a = []

    for c in b:
        a.append(c)

    api_data = {'hi': 'ok',
                'a': a
                }
    return HttpResponse(json.dumps(api_data, indent=4), content_type="application/json")
