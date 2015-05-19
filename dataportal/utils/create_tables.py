import os
import pprint
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiserd.settings")

from dataportal import models

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


build_ztab_table()