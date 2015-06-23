__author__ = 'ubuntu'


class NewDBRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):

        """
        Attempts to read auth models go to auth_db.
        """
        print model._meta.object_name + 'bbbb'

        # print model._meta, model._meta.app_label

        if model._meta.app_label == 'newtables':
            print 'using new'
            return 'new'
        return 'default'

    def db_for_write(self, model, **hints):

        """
        Attempts to write auth models go to auth_db.
        """
        print model._meta.object_name + 'aaaa'

        # print model._meta, model._meta.app_label

        if model._meta.app_label == 'newtables':
            print 'using new'
            return 'new'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'new' or \
           obj2._meta.app_label == 'new':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):

        # print model._meta.app_label + ' old'
        # print model._meta
        # print model._meta.db_table + ' old'
        # print model._meta.object_name + ' old'
        # print '\n'

        # """
        # Make sure the auth app only appears in the 'auth_db'
        # database.
        # """

        # print app_label, db, model
        if app_label == 'newtables':
            # print app_label, db, db == 'new', model._meta.object_name, '\n'
            return db == 'new'
        return None
