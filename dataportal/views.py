import json
import pprint
from random import Random
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

    # return render(request, 'survey_data.html',
    #               {'data': True,
    #                'msg': 'msg',
    #                'survey_data': surveys,
    #                'survey_data_format': surveys_format},
    #               context_instance=RequestContext(request))

    return HttpResponse(json.dumps(surveys, indent=4), content_type="application/json")


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

@csrf_exempt
def get_metadata(request):

    print request.POST
    data = []
    rnd = Random()
    table = request.POST.get('table', 'no_table')

    for i in range(0, rnd.randint(5, 50)):
        data.append({
            'a': str(rnd.randint(1, 10)) + table,
            'b': str(rnd.randint(1, 10)) + table,
            'c': str(rnd.randint(1, 10)) + table,
            'd': str(rnd.randint(1, 10)) + table,
            'e': str(rnd.randint(1, 10)) + table
        })

    response_data = {
        'data': data,
        'post': request.POST.__dict__
    }
    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def map_search(request):
    return render(request, 'map_search.html', {}, context_instance=RequestContext(request))


@csrf_exempt
def spatial_search(request):

    test_available = True

    response_data = {
        'data': []
    }

    geography_wkt = request.POST.get('geography', '')
    if test_available and (len(request.POST.get('test', '')) or len(geography_wkt) == 0):
        response_data = {'data': [{'area': u'Wales', 'survey_short_title': u'WERS', 'date': '2005 / 04 / 30', 'survey_id': u'sid_wersmq2004', 'survey_id_full': u'sid_wersmq2004                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_412', 'survey_id_full': u'sid_whs2008_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': '', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_03', 'survey_id_full': u'sid_whs2007_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Gwent, Monmouthshire, South East Wales, NP152, South Wales, W01001581', 'survey_short_title': u'LiW Property', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwps2004', 'survey_id_full': u'sid_liwps2004                                                                                                                                                                                                                                                  ', 'areas': [u'NP152', u'Gwent', u'South East Wales', u'Monmouthshire', u'South Wales', u'W01001581']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_03', 'survey_id_full': u'sid_whs2009_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007aq', 'survey_id_full': u'sid_whs2007aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2005 / 09 / 30', 'survey_id': u'sid_whs0306aq', 'survey_id_full': u'sid_whs0306aq                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_03', 'survey_id_full': u'sid_whs2008_03                                                                                                                                                                                                                                                 ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008aq', 'survey_id_full': u'sid_whs2008aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_1315', 'survey_id_full': u'sid_whs2007_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2007 / 07 / 31', 'survey_id': u'sid_liw2007', 'survey_id_full': u'sid_liw2007                                                                                                                                                                                                                                                    ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire 005E', u'Monmouth', u'Gwent', u'Monmouthshire']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2008 / 12 / 31', 'survey_id': u'sid_whs2008_1315', 'survey_id_full': u'sid_whs2008_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_412', 'survey_id_full': u'sid_whs2009_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009aq', 'survey_id_full': u'sid_whs2009aq                                                                                                                                                                                                                                                  ', 'areas': []}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2007 / 12 / 31', 'survey_id': u'sid_whs2007_412', 'survey_id_full': u'sid_whs2007_412                                                                                                                                                                                                                                                ', 'areas': []}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2006 / 10 / 13', 'survey_id': u'sid_liwhh2006', 'survey_id_full': u'sid_liwhh2006                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'South Wales', u'Monmouthshire 005E', u'South East Wales', u'NP151']}, {'area': u'Monmouthshire', 'survey_short_title': u'Welsh Health Survey', 'date': '2009 / 12 / 31', 'survey_id': u'sid_whs2009_1315', 'survey_id_full': u'sid_whs2009_1315                                                                                                                                                                                                                                               ', 'areas': []}, {'area': u'Monmouthshire 005E, Monmouthshire, Monmouth, NP151, South East Wales, South Wales', 'survey_short_title': u'LiW Household', 'date': '2004 / 10 / 04', 'survey_id': u'sid_liwhh2004', 'survey_id_full': u'sid_liwhh2004                                                                                                                                                                                                                                                  ', 'areas': [u'South Wales', u'NP151', u'Monmouthshire', u'South East Wales', u'Monmouthshire 005E', u'Monmouth']}, {'area': u'Monmouthshire 005E, Gwent, Monmouthshire, Monmouth, NP151, South Wales', 'survey_short_title': u'LiW Household', 'date': '2005 / 08 / 14', 'survey_id': u'sid_liwhh2005', 'survey_id_full': u'sid_liwhh2005                                                                                                                                                                                                                                                  ', 'areas': [u'Monmouthshire', u'Gwent', u'Monmouth', u'NP151', u'South Wales', u'Monmouthshire 005E']}], 'success': True}
        return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")
    elif len(geography_wkt) == 0:
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
    survey_info = {}

    for geoms in tables:
        f_table_name = geoms[0]
        print f_table_name
        f_geometry_column = geoms[1]

        survey_data = {}
        survey_data['areas'] = []

        intersects = "SELECT area_name from " + f_table_name + \
                     " WHERE ST_Intersects(ST_Transform(ST_GeometryFromText('" + geography_wkt + "', 27700), 4326)," + f_geometry_column + ")"

        cursor.execute(intersects)
        area_names = cursor.fetchall()

        area_name = ''
        if len(area_names) > 0:
            # print area_names[0][0].strip()
            areas.append(area_names[0][0])
            area_name = area_names[0][0]
        survey_data['area'] = area_name

        spatials = models.survey_models.SurveySpatialLink.objects.using('survey').filter(spatial_id=geoms[0]).values_list('surveyid', flat=True)

        spatials = list(spatials)

        date = ''
        sid = ''
        survey_short_title = ''
        if len(spatials) > 0:
            # print spatials[0].strip()
            survey_ids.append(spatials[0].strip())
            sid = spatials[0]
            survey_model = models.survey_models.Survey.objects.using('survey').filter(surveyid__in=spatials).values_list('short_title', 'collectionenddate', 'surveyid').distinct()

            for s in survey_model:
                if len(s) > 0:
                    survey_short_title = s[0]
                try:
                    date = s[1].strftime('%Y / %m / %d')
                except:
                    date = ''

        survey_data['survey_short_title'] = survey_short_title
        survey_data['survey_id'] = sid.strip()
        survey_data['survey_id_full'] = sid
        survey_data['date'] = date

        if len(survey_data['survey_id']):
            if survey_info.has_key(survey_data['survey_id']):
                survey_info[survey_data['survey_id']]['areas'].append(survey_data['area'])
                survey_info[survey_data['survey_id']]['area'] = ', '.join(list(set(survey_info[survey_data['survey_id']]['areas'])))
            else:
                survey_info[survey_data['survey_id']] = survey_data

    # response_data['areas'] = areas
    response_data['data'] = survey_info.values()

    # cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
    # max_value = cursor.fetchone()[0]

    print response_data

    return HttpResponse(json.dumps(response_data, indent=4), content_type="application/json")


def test(request):
    return render(request, 'test.html',
                  {'data': True, 'msg': 'msg'},
                  context_instance=RequestContext(request))
