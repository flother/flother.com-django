from django.db.models import Manager


class FileManager(Manager):

    """
    Django model manager for the File model. Overrides the default
    latest() method so it returns the latest visible file, and adds a
    visible() method that returns only visible files.
    """

    def latest(self, field_name=None):
        """Return the latest visible file."""
        return self.visible().latest(field_name)

    def visible(self, **kwargs):
        """
        Return a QuerySet that contains only those files that are 
        visible, i.e. files with a status of "visible".
        """
        from flother.apps.files.models import File
        return self.get_query_set().filter(is_visible=True, **kwargs)
