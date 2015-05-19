from django.db import models

__author__ = 'ubuntu'

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('new',)


class Response(models.Model):
    question_id = models.CharField(max_length=255)

    class Meta():
        new = True
        app_label = 'new'


class ResponseDescription(models.Model):
    response = models.ForeignKey('Response')
    question_result_id = models.CharField(max_length=255)
    answer_term_id = models.IntegerField()
    answer_term = models.CharField(max_length=255)

    class Meta():
        new = True
        app_label = 'new'


class ResponseOption(models.Model):
    responseDescription = models.ForeignKey('ResponseDescription')
    answer_term_id = models.IntegerField()
    answer_option = models.CharField(max_length=255)

    class Meta():
        new = True
        app_label = 'new'