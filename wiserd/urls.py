"""wiserd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dataportal import views
urlpatterns = [

    url(r'^$', views.index, name='home'),

    url(r'^test', views.test, name='test'),

    url(r'^about_us', views.index, name='about_us'),
    url(r'^software', views.index, name='software'),
    url(r'^help', views.index, name='help'),

    url(r'^profile', views.index, name='user_profile_home'),
    url(r'^login', views.login, name='account_login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^do_login', views.do_login, name='login.do_login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^do_signup', views.do_signup, name='signup.do_signup'),

    url(r'^do_advanced_search', views.do_advanced_search, name='do_advanced_search'),
    url(r'^search_advanced', views.search_advanced, name='search_advanced'),

    url(r'^map_search', views.map_search, name='map_search'),

    url(r'^data_autocomplete', views.data_autocomplete, name='data.autocomplete'),
    # url(r'^get_metadata', views.get_metadata, name='data.get_metadata'),
    # url(r'^metadata/survey/(?P<wiserd_id>\S+)', views.get_metadata, name='data.get_metadata'),

    url(r'^metadata/dublin_core', views.dc_info, name='dc_info'),

    url(r'^metadata/survey/dublin_core/(?P<wiserd_id>\S+)', views.survey_dc_data, name='survey_dc_data'),
    url(r'^metadata/survey/questions/(?P<wiserd_id>\S+)', views.survey_questions, name='survey_questions'),
    url(r'^metadata/survey/(?P<wiserd_id>\S+)', views.survey_metadata, name='survey_metadata'),

    url(r'^spatial_search', views.spatial_search, name='spatial_search'),
    url(r'^search_survey_question_gui/(?P<search_terms>\S+)',
        views.search_survey_question_gui, name='search_survey_question_gui'),

    url(r'^metadata/search/survey/questions/(?P<search_terms>\S+)',
        views.search_survey_question, name='search_survey_question'),

    url(r'^admin/', include(admin.site.urls)),

]


urlpatterns += staticfiles_urlpatterns()
