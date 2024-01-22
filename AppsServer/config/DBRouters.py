class DjangoDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'config':
            return 'my_app_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'config':
            return 'my_app_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'config' and \
                obj2._meta.app_label == 'config':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'my_app_db':
            if model._meta.app_label == 'config':
                return True
        elif model._meta.app_label == 'config':
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'config':
            return db == 'my_app_db'
        return None
