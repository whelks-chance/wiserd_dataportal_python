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

    fields = ["questionnumber", "updated", "literal_question_text", "variableid", "qtext_index", "link_from_question_id", "qid", "thematic_tags", "subof_id", "user_id_id", "subof_question_id", "thematic_groups", "created", "link_from_id", "type_id", "survey_id", "notes", "thematic_groups_set"]

    b2 = models.Question.objects.using('new').all().prefetch_related('thematic_groups_set')

    a2 = []

    for c2 in b2:
        d = {}
        for f in fields:
            d[f] = getattr(c2, f)

            thematic_groups_set = []
            for tg in c2.thematic_groups_set.all().values():
                thematic_groups_set.append(tg)

            d['thematic_groups_set'] = thematic_groups_set

            thematic_tags_set = []
            for tag in c2.thematic_tags_set.all().values():
                thematic_tags_set.append(tag)

            d['thematic_tags_set'] = thematic_tags_set
        a2.append(d)

    api_data = {'hi': 'ok',
                'a': a,
                'questions': a2
                }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")
