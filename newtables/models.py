from django.db import models

__author__ = 'ubuntu'

# import django.db.models.options as options
# options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('new',)


class NewSurvey(models.Model):
    surveyid = models.CharField(max_length=255)
    identifier = models.CharField(max_length=50)
    survey_title = models.TextField(blank=True, null=True)
    datacollector = models.CharField(max_length=50, blank=True, null=True)
    collectionstartdate = models.DateField(blank=True, null=True)
    collectionenddate = models.DateField(blank=True, null=True)
    moc_description = models.TextField(blank=True, null=True)
    samp_procedure = models.TextField(blank=True, null=True)
    collectionsituation = models.TextField(blank=True, null=True)
    surveyfrequency = models.CharField(max_length=255, blank=True, null=True)
    surveystartdate = models.DateField(blank=True, null=True)
    surveyenddate = models.DateField(blank=True, null=True)
    des_weighting = models.TextField(blank=True, null=True)
    samplesize = models.CharField(max_length=100, blank=True, null=True)
    responserate = models.CharField(max_length=20, blank=True, null=True)
    descriptionofsamplingerror = models.TextField(blank=True, null=True)
    dataproduct = models.CharField(max_length=255, blank=True, null=True)
    dataproductid = models.CharField(max_length=25, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    long = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)
    spatialdata = models.NullBooleanField()

    class Meta:
        # managed = False
        db_table = 'new_survey'
        # app_label = 'new'


class NewResponse(models.Model):
    question_id = models.CharField(max_length=255)

    class Meta():
        db_table = 'new_response'
        # new = True
        # app_label = 'new'


class NewResponseDescription(models.Model):
    response = models.ForeignKey('NewResponse')
    question_result_id = models.CharField(max_length=255)
    answer_term_id = models.IntegerField()
    answer_term = models.CharField(max_length=255)

    class Meta():
        db_table = 'new_response_description'
        # new = True
        # app_label = 'new'


class NewResponseOption(models.Model):
    responseDescription = models.ForeignKey('NewResponseDescription')
    answer_term_id = models.IntegerField()
    answer_option = models.CharField(max_length=255)

    class Meta():
        # new = True
        db_table = 'new_response_option'
        # app_label = 'new'