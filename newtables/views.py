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

    q_fields = ["questionnumber", "updated", "literal_question_text", "variableid", "qtext_index", "link_from_question_id", "qid", "thematic_tags", "subof_id", "user_id_id", "subof_question_id", "thematic_groups", "created", "link_from_id", "type_id", "survey_id", "notes", "thematic_groups_set"]
    r_fields = ["responseid", "responsetext", "response_type", "routetype", "table_ids", "computed_var", "checks", "route_notes", "user_id", "created", "updated"]
    res_type_fields = ["responseid", "response_name", "response_description"]

    b2 = models.Question.objects.using('new').all().prefetch_related('thematic_groups_set', 'response')[:10]

    a2 = []

    for c2 in b2:
        d = {}
        for f in q_fields:
            d[f] = getattr(c2, f)

            thematic_groups_set = []
            for tg in c2.thematic_groups_set.all().values():
                thematic_groups_set.append(tg)

            d['thematic_groups_set'] = thematic_groups_set

            thematic_tags_set = []
            for tag in c2.thematic_tags_set.all().values():
                thematic_tags_set.append(tag)

            d['thematic_tags_set'] = thematic_tags_set

            res = {}
            for r in r_fields:
                r_var = getattr(c2.response, r)
                # print type(r_var)

                if 'models.ResponseType' in str(type(r_var)):
                    res_type = {}
                    for r_t_f in res_type_fields:
                        res_type[r_t_f] = getattr(c2.response.response_type, r_t_f)
                    res['response_type'] = res_type
                else:
                    res[r] = r_var

            d['response'] = res
            a2.append(d)

    api_data = {'hi': 'ok',
                'a': a,
                'questions': a2
                }
    return HttpResponse(json.dumps(api_data, indent=4, default=date_handler), content_type="application/json")
