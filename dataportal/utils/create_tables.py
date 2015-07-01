import os
import pprint
from django.db import connections, ConnectionRouter, DEFAULT_DB_ALIAS

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd.settings")

from dataportal import models
from newtables import models as new_models

__author__ = 'ubuntu'

import django
django.setup()

def build_ztab_table():

    # query = 'select table_name from information_schema.tables where table_name like %s limit 10'
    # variables = ['ztab_']

    # ztab_tables = models.ztabResponseOptions.objects.db_manager().raw(query, variables)

    from django.db import connection

    cursor = connections['survey'].cursor()

    # qid = 'qid_liw2007q51-s1'
    #
    # cursor.execute("Select table_name, column_name from information_schema.columns " +
    #                "where lower(table_name) in " +
    #                "(select lower(table_ids) from responses where responseID = " +
    #                "( SELECT responseID FROM questions_responses_link where qid = %s)) " +
    #                "and column_name != 'table_pk' and column_name != 'user_id' and " +
    #                "column_name != 'date_time' and column_name != 'res_table_id'", [qid, ])
    #
    # ztab_from_qid = cursor.fetchall()

    cursor.execute("select table_name from information_schema.tables where table_name like %s limit 30", ['ztab%'])
    # max_value = cursor.fetchone()[0]
    ztab_tables = cursor.fetchall()

    print ztab_tables

    for table in ztab_tables:
        print '\n'
        print table
        cursor.execute("select column_name from information_schema.columns where table_name = %s " +
                       "and column_name != 'table_pk' and column_name != 'user_id' and " +
                       "column_name != 'date_time' and column_name != 'res_table_id'", [table[0],])
        column_headers = cursor.fetchall()

        print [a[0] for a in column_headers]

        cursor.execute('select * from ' + table[0], [])
        # print cursor.fetchall()

        desc = cursor.description
        # print pprint.pformat(desc)
        desc_dict = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        # print pprint.pformat(desc_dict, indent=4)

        for option in desc_dict:
            print '\n'
            for header in column_headers:
                print header[0], option[header[0]]

    return True


def get_question_number(qid_start):
    number_string_array = []

    done = False
    while not done:
        if qid_start[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            number_string_array.insert(0, qid_start[-1])
            qid_start = qid_start[0:-1]
        else:
            done = True
    return ''.join(number_string_array), qid_start


def find_parents():

    found_count = 0

    # esseses = ['sssss', 'ssssss', 'sssssss', 'ssssssss', 'sssssssss', 'ssssssssss']

    num_ses = 12

    complete = []

    while num_ses > 3:
        num_ses -= 1

        esses = ''.join('s' for a in range(0, num_ses))
        questions_models = models.survey_models.Questions.objects.using('survey').filter(qid__endswith=esses).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

        print esses, len(esses), len(questions_models)

        one_less_s = ''.join('s' for a in range(0, (num_ses-1)))

        for question in questions_models:
            if question['qid'].strip() not in complete:
                qid = question['qid']

                complete.append(qid.strip())

                print qid.strip()

                qid_start = qid.strip().split('-s')[0]

                question_number, qid_start_without_number = get_question_number(qid_start)

                potential_child_qid = qid_start_without_number + str(int(question_number) -1) + '-' + one_less_s

                questions_parent_models = models.survey_models.Questions.objects.using('survey').filter(qid__startswith=potential_child_qid).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

                if len(questions_parent_models):
                    for parent_question in questions_parent_models:
                        print '*' + parent_question['qid'].strip() + '*'

                        found_count += 1
                else:
                    potential_child_qid_non_decrement = qid_start + '-' + one_less_s
                    questions_parent_models = models.survey_models.Questions.objects.using('survey').filter(qid__startswith=potential_child_qid_non_decrement).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

                    for parent_question in questions_parent_models:
                        print '*-*' + parent_question['qid'].strip() + '*-*'

                        found_count += 1


                print '\n'
    print found_count
    print len(complete)


def find_orphans():

    questions_models = models.survey_models.Questions.objects.using('survey').values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")
    print questions_models.count()

    for question in questions_models:
        question_id = question['qid']
        question_id = question_id.strip()

        question_response_link_models = models.survey_models.QuestionsResponsesLink.objects.using('survey').all().filter(qid__icontains=question_id).values('responseid')

        question_responses = []
        columns = []

        if len(question_response_link_models):
            question_response_models = models.survey_models.Responses.objects.using('survey').all().filter(responseid__in=question_response_link_models).values()

            if question_response_models[0]['table_ids'] != u'N/A':

                # print type(u'N/A'), u'N/A', type(question_response_models[0]['table_ids']), question_response_models[0]['table_ids']

                # print '*' + 'N/A' + '* ' + '*' + question_response_models[0]['table_ids'] + '*'
                #
                # print u'N/A' == question_response_models[0]['table_ids']

                try:
                    cursor = connections['survey'].cursor()
                    cursor.execute("select * from " + question_response_models[0]['table_ids'])
                    ztab_tables = cursor.fetchall()

                    # print ztab_tables

                    for question_response_model in ztab_tables:
                        question_responses.append(question_response_model)

                    # cursor.execute("select column_name from information_schema.columns where table_name = '" + question_response_models[0]['table_ids'] + "'")
                    # column_names = cursor.fetchall()
                    #
                    # # print column_names
                    #
                    # for column_data in column_names:
                    #     columns.append(column_data[0])
                except Exception as e:
                    print e

        print question_id, len(question_responses)


def clean_str(input):
    return str(input or '').strip()


def make_freqs():
    survey_frequecy_models = models.survey_models.SurveyFrequency.objects.using('survey').all().values()
    for f in survey_frequecy_models:
        freq_id = clean_str(f['svyfreqid'])
        new_survey_freq, created = new_models.SurveyFrequency.objects.using('new').get_or_create(svyfreqid=freq_id)
        if created:
            new_survey_freq.svy_frequency_title = clean_str(f['svy_frequency_title'])
            new_survey_freq.svy_frequency_description = clean_str(f['svy_frequency_description'])
            new_survey_freq.save(using='new')
        else:
            print 'already has ' + freq_id


def make_q_types():
    question_types = models.survey_models.QType.objects.using('survey').all().values()
    for f in question_types:
        q_type_id = clean_str(f['q_typeid'])
        new_question_types, created = new_models.QType.objects.using('new').get_or_create(q_typeid=q_type_id)
        if created:
            new_question_types.q_type_text = clean_str(f['q_type_text'])
            new_question_types.q_typedesc = clean_str(f['q_typedesc'])
            new_question_types.save(using='new')
        else:
            print 'already has ' + q_type_id


def make_thematic_groups():
    group = models.survey_models.ThematicGroups.objects.using('survey').all().values()
    for g in group:
        group_id = clean_str(g['tgroupid'])
        new_thematic_group, created = new_models.ThematicGroup.objects.using('new').get_or_create(tgroupid=group_id)
        if created:
            new_thematic_group.grouptitle = clean_str(g['grouptitle'])
            new_thematic_group.groupdescription = clean_str(g['groupdescription'])
            new_thematic_group.save(using='new')
        else:
            print 'already has group' + group_id


def make_thematic_tags():
    group_tags = models.survey_models.GroupTags.objects.using('survey').all().values()
    for f in group_tags:
        tag_id = clean_str(f['tagid'])
        new_thematic_tag, created = new_models.ThematicTag.objects.using('new').get_or_create(tagid=tag_id)
        if created:
            thematic_group = new_models.ThematicGroup.objects.using('new').get(tgroupid=clean_str(f['tgroupid']))

            new_thematic_tag.thematic_group = thematic_group
            new_thematic_tag.tag_text = clean_str(f['tag_text'])
            new_thematic_tag.tag_description = clean_str(f['tag_description'])
            new_thematic_tag.save(using='new')
        else:
            print 'already has ' + tag_id


def make_users():
    users = models.survey_models.UserDetails.objects.using('survey').all().values()
    for f in users:
        user_id = clean_str(f['user_id'])
        new_user, created = new_models.UserDetail.objects.using('new').get_or_create(user_id=user_id)
        if created:
            new_user.user_name = clean_str(f['user_name'])
            new_user.user_email = clean_str(f['user_email'])
            new_user.save(using='new')
        else:
            print 'already has ' + user_id


def find_surveys():

    fails = []

    survey_model_ids = models.survey_models.Survey.objects.using('survey').all().values()[:1]

    # print survey_model_ids

    for s in survey_model_ids:
        clean_sid = s['surveyid'].strip().lower()

        new_survey, created = new_models.Survey.objects.using('new').get_or_create(surveyid=clean_sid)

        if created:
            frequency = new_models.SurveyFrequency.objects.using('new').get(survey_frequency_description=s['svy_frequency_description'].strip())
            new_survey.frequency = frequency

            user = new_models.UserDetail.objects.using('new').get(user_id=s['user_id'].strip())
            new_survey.user = user

            # new_survey.surveyid = clean_str(s['surveyid'])
            new_survey.identifier = clean_str(s['identifier'])
            new_survey.survey_title = clean_str(s['survey_title'])
            new_survey.datacollector = clean_str(s['datacollector'])

            new_survey.collectionstartdate = s['collectionstartdate']
            new_survey.collectionenddate = s['collectionenddate']

            new_survey.moc_description = clean_str(s['moc_description'])
            new_survey.samp_procedure = clean_str(s['samp_procedure'])
            new_survey.collectionsituation = clean_str(s['collectionsituation'])
            new_survey.surveyfrequency = clean_str(s['surveyfrequency'])

            new_survey.surveystartdate = s['surveystartdate']
            new_survey.surveyenddate = s['surveyenddate']

            new_survey.des_weighting = clean_str(s['des_weighting'])
            new_survey.samplesize = clean_str(s['samplesize'])
            new_survey.responserate = clean_str(s['responserate'])
            new_survey.descriptionofsamplingerror = clean_str(s['descriptionofsamplingerror'])
            new_survey.dataproduct = clean_str(s['dataproduct'])
            new_survey.dataproductid = clean_str(s['dataproductid'])
            new_survey.location = clean_str(s['location'])
            new_survey.link = clean_str(s['link'])
            new_survey.notes = clean_str(s['notes'])
            new_survey.user_id = clean_str(s['user_id'])

            new_survey.created = s['created']
            new_survey.updated = s['updated']

            new_survey.long = clean_str(s['long'])
            new_survey.short_title = clean_str(s['short_title'])
            new_survey.spatialdata = (s['spatialdata'] == 'y')
            new_survey.survey_title = clean_str(s['survey_title'])

            new_survey.save(using='new')
        else:
            print 'already has survey ' + clean_sid

        survey_question_link_models = models.survey_models.SurveyQuestionsLink.objects.using('survey').all().filter(surveyid=s['surveyid']).values_list('qid', flat=True)

        for ql in survey_question_link_models:

            print ql

            questions_models = models.survey_models.Questions.objects.using('survey').filter(qid=ql).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

            for q in questions_models:
                print '\n\n'
                # print q
                clean_q = q['qid'].strip().lower()

                new_question, q_created = new_models.Question.objects.using('new').get_or_create(qid=clean_q, survey=new_survey)
                if q_created or True:

                    # try:
                    q_type = new_models.QType.objects.using('new').get(q_type_text= clean_str(q['type']))
                    user = new_models.UserDetail.objects.using('new').get(user_id= clean_str(q['user_id']))

                    new_question.thematic_groups = clean_str(q['thematic_groups'])

                    thematic_tags = ''
                    if 'System.Windows' not in clean_str(q['thematic_tags']):
                        thematic_tags = clean_str(q['thematic_tags'])
                    new_question.thematic_tags = thematic_tags

                    # new_question.link_from = q['link_from']
                    # new_question.subof = q['subof']

                    new_question.literal_question_text = clean_str(q['literal_question_text'])
                    new_question.questionnumber = clean_str(q['questionnumber'])
                    new_question.type = q_type
                    new_question.variableid = clean_str(q['variableid'])
                    new_question.notes = clean_str(q['notes'])
                    new_question.user_id = user
                    new_question.created = q['created']

                    if len(q['thematic_groups'].strip()):
                        for tg in q['thematic_groups'].strip().split(','):
                            tg_model = new_models.ThematicGroup.objects.using('new').get(grouptitle=tg.strip())
                            new_question.thematic_groups_set.add(tg_model)

                    if len(q['thematic_tags'].strip()):
                        for tag in q['thematic_tags'].strip().split(','):
                            if 'System.Windows' not in tag:
                                print '***' + tag
                                tag_model = new_models.ThematicTag.objects.using('new').get(tag_text=tag.strip())
                                new_question.thematic_tags_set.add(tag_model)

                    new_question.save(using='new')

                    # except Exception as e:
                    #     print 'failed on ' + clean_q + ' ' + str(e)
                    #     fails.append(clean_q)
                else:
                    print 'already has q_ ' + clean_q

    print fails

# make_freqs()
# make_q_types()
# make_users()
# make_thematic_groups()
# make_thematic_tags()
find_surveys()

# find_orphans()

# find_parents()

# build_ztab_table()