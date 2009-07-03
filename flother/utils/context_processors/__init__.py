import datetime


def section(request):
    """
    Add a ``section`` variable to the template context, to hold the
    current section of the web site.
    """
    return {
        'section': request.path[1:-1].split('/')[0] or 'home'
    }


def current_year(request):
    """
    Add a variable to the template context that contains the current
    year.
    """
    return {
        'current_year': datetime.date.today().year,
    }
