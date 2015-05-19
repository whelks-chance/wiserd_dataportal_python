import json
import pprint
from django.contrib import auth
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
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
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_metadata(request):
    response_data = {}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def map_search(request):
    return render(request, 'map_search.html', {}, context_instance=RequestContext(request))
