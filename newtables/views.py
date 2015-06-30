import json
from django.http import HttpResponse

# Create your views here.
from dataportal.views import date_handler
from newtables import models


def newdb(request):
    b = models.Survey.objects.using('new').all().values()

    a = []

    for c in b:
        a.append(c)

    b2 = models.Question.objects.using('new').all().values()

    a2 = []

    for c2 in b2:
        a2.append(c2)
        # print c2.thematic_groups_set.all().using('new').values()

    api_data = {'hi': 'ok',
                'a': a,
                'questions': a2
                }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")
