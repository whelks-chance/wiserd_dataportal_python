import json
import pprint
from django.contrib import auth
from django.db import connections
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from dataportal import models


def index(request):
    return render(request, 'home.html',
                  {'data': True, 'msg': 'msg'},
                  context_instance=RequestContext(request))


def dc_info(request):

    dc_models = models.survey_models.DcInfo.objects.using('survey').all()

    print dc_models.query

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

    # survey_link = models.QuestionLink

    # print wiserd_id

    wiserd_id = wiserd_id.strip()

    # survey_models = models.survey_models.Survey.objects.using('survey').all().filter(identifier__icontains=wiserd_id).values_list('surveyid', 'identifier', 'survey_title')
    survey_models = models.survey_models.Survey.objects.using('survey').all().filter(identifier__icontains=wiserd_id).values_list("surveyid", "identifier", "survey_title", "datacollector", "collectionstartdate", "collectionenddate", "moc_description", "samp_procedure", "collectionsituation", "surveyfrequency", "surveystartdate", "surveyenddate", "des_weighting", "samplesize", "responserate", "descriptionofsamplingerror", "dataproduct", "dataproductid", "location", "link", "notes", "user_id", "created", "updated", "long", "short_title", "spatialdata")

    print survey_models.query

    surveys = []

    # print survey_models

    for survey_model in survey_models:
        print survey_model
        surveys.append({
            'data': survey_model
        })

    surveys_format = pprint.pformat(survey_models, indent=4)

    return render(request, 'survey_data.html',
                  {'data': True,
                   'msg': 'msg',
                   'survey_data': surveys,
                   'survey_data_format': surveys_format},
                  context_instance=RequestContext(request))


def login(request):
    return render(request, 'login.html',
                  context_instance=RequestContext(request))


def logout(request):
    logout_success = False
    msg = 'Auth Error, please refresh the page'
    if request.user.is_authenticated():
        auth.logout(request)
        msg = 'You have successfully logged out'
        logout_success = True
    #do logout
    return render(request, 'home.html',
                  {'logout_success': logout_success, 'msg': msg},
                  context_instance=RequestContext(request))


def do_login(request):
    print request.POST
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
            auth.login(request, user)
            success = True
            msg = 'You have successfully logged in'
        else:
            print("The password is valid, but the account has been disabled!")
            success = False
            msg = 'This account has been disabled. Please contact the Lost-Visions team.'

        return render(request, 'home.html',
                      {'login_success': success, 'msg': msg},
                      context_instance=RequestContext(request))
    else:
        msg = 'Username and Password combination not recognised, please try again.'
        success = False

        return render(request, 'login.html',
                      {'login_success': success, 'msg': msg},
                      context_instance=RequestContext(request))


def signup(request):
    return render(request, 'signup.html', context_instance=RequestContext(request))


def do_signup(request):
    print request.POST
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print("User is valid, active and authenticated")
            auth.login(request, user)
            success = True
            msg = 'You have successfully logged in'
        else:
            print("The password is valid, but the account has been disabled!")
            success = False
            msg = 'This account has been disabled. Please contact the Lost-Visions team.'

        return render(request, 'home.html',
                      {'login_success': success, 'msg': msg},
                      context_instance=RequestContext(request))
    else:
        msg = 'Username and Password combination not recognised, please try again.'
        success = False

        return render(request, 'login.html',
                      {'login_success': success, 'msg': msg},
                      context_instance=RequestContext(request))


def search_advanced(request):
    return render(request, 'search_advanced.html', {}, context_instance=RequestContext(request))


def do_advanced_search(request):
    response_data = []
    readable_query = ''
    all_survey_ids = []
    number_of_results_int = 100
    return render(request, 'advanced_search_results.html',
              {'results': response_data,
               'query_array': request.GET,
               'query': readable_query,
               'all_survey_ids': all_survey_ids,
               'number_to_show': number_of_results_int},
              context_instance=RequestContext(request))



def data_autocomplete(request):
    response_data = {}
    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def get_metadata(request):
    response_data = {}
    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def map_search(request):
    return render(request, 'map_search.html', {}, context_instance=RequestContext(request))


@csrf_exempt
def spatial_search(request):

    response_data = {}

    geography = request.POST.get('geography', '')
    if len(geography) == 0:
        response_data['success'] = False
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")

    response_data['success'] = True

    cursor = connections['survey'].cursor()

    table_cols = "SELECT DISTINCT f_table_name, f_geometry_column FROM geometry_columns where f_table_schema = 'public'"
    cursor.execute(table_cols)
    tables = cursor.fetchall()
    print tables

    areas = []
    survey_ids = []
    survey_info = []

    for geoms in tables:
        survey_data = {}

        intersects = "SELECT area_name from " + geoms[0] + \
        " WHERE ST_Intersects(ST_Transform(ST_GeometryFromText('" + geography + "', 27700), 4326)," + geoms[1] + ")"

        cursor.execute(intersects)
        area_names = cursor.fetchall()

        if len(area_names) > 0:
            # print area_names
            areas.append(area_names[0])
            survey_data['areas'] = area_names

        spatials = models.survey_models.SurveySpatialLink.objects.using('survey').filter(spatial_id=geoms[0]).values_list('surveyid', flat=True)

        spatials = list(spatials)

        if len(spatials) > 0:
            print spatials
            print spatials[0].strip()
            survey_ids.append(spatials[0].strip())
            survey_data['survey_ids'] = spatials

            survey_model = models.survey_models.Survey.objects.using('survey').filter(surveyid__in=spatials).values_list('short_title', 'collectionenddate')

            print survey_model

            for s in survey_model:

                if len(s) > 0:
                    print type(s[0]), s[0]
                    survey_data['survey_short_title'] = s[0]
                try:
                    date = s[1].strftime('%Y-%m-%d %H:%M:%S %Z')
                except:
                    date = ''
                survey_data['date'] = date

        survey_info.append(survey_data)

    # response_data['areas'] = areas
    response_data['surveys'] = survey_info

    # cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
    # max_value = cursor.fetchone()[0]

    print response_data

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
