import os
import pprint
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd.settings")

from dataportal import models
from newtables import models as new_models

__author__ = 'ubuntu'


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


def find_surveys():

    survey_model_ids = models.survey_models.Survey.objects.using('survey').all().values()[:1]

    print survey_model_ids

    for s in survey_model_ids:
        clean_sid = s['surveyid'].strip().lower()

        new_survey, created = new_models.Survey.objects.using('new').get_or_create(surveyid=clean_sid)
        # new_survey.surveyid = clean_sid
        new_survey.survey_title = s['survey_title']
        new_survey.save(using='new')

        print s

        survey_question_link_models = models.survey_models.SurveyQuestionsLink.objects.using('survey').all().filter(surveyid=s['surveyid']).values_list('qid', flat=True)

        for ql in survey_question_link_models:

            print ql

            questions_models = models.survey_models.Questions.objects.using('survey').filter(qid=ql).values("qid", "literal_question_text", "questionnumber", "thematic_groups", "thematic_tags", "link_from", "subof", "type", "variableid", "notes", "user_id", "created", "updated", "qtext_index")

            for q in questions_models:
                print q

                new_question = new_models.Question()
                new_question.qid = q['qid']
                new_question.survey = new_survey
                new_question.save(using='new')

find_surveys()

# find_orphans()

# find_parents()

# build_ztab_table()