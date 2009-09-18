from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.utils import simplejson

from flother.apps.files.models import File


@permission_required('files.can_use', '/admin/')
def files_list(request):
    """
    Return a list of available files as a JSON object.  This is used
    only in the admin to allow files to be inserted into Markdown-based
    textareas.
    """
    files = [{
        'id': f.id,
        'title': f.title,
        'url': f.get_absolute_url(),
        'uploaded_at': f.uploaded_at.isoformat(),
        'thumbnail_html': f.thumbnail_html()
    } for f in File.objects.visible()]
    return HttpResponse(simplejson.dumps(files), 'application/json')
