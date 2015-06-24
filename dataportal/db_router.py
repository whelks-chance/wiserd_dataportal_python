__author__ = 'ubuntu'


class OldDBRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):

        """
        Attempts to read auth models go to auth_db.
        """

        if model._meta.app_label == 'dataportal':
            print 'using new'
            return 'survey'
        return 'default'

    def db_for_write(self, model, **hints):

        """
        Attempts to write auth models go to auth_db.
        """

        if model._meta.app_label == 'dataportal':
            print 'using new'
            return 'survey'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):

        print obj1, obj2, '*****2'
        # """
        # Allow relations if a model in the auth app is involved.
        # """
        if obj1._meta.app_label == 'dataportal' and \
           obj2._meta.app_label == 'dataportal':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):

        # print model._meta.app_label + ' old'
        # print app_label
        # print model._meta
        # print model._meta.db_table + ' old'
        # print model._meta.object_name + ' old'
        # print '\n'

        # """
        # Make sure the auth app only appears in the 'auth_db'
        # database.
        # """

        # print app_label, db, model
        if app_label == 'dataportal':
            return db == 'survey'
        return None