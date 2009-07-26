# -*- coding: utf-8 -*-
import urllib
import urllib2

from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson


def search_results(request):
    """Return a list of pages that contain the given search term"""
    search_query = request.GET.get('q')
    try:
        page = int(request.GET.get('p', 1))
    except ValueError:
        page = 1
    search_results = []
    total_pages = 0
    current_page = False
    next_page = False
    previous_page = False
    if search_query:
        # Get the current site and build the Google Ajax search URL.
        site = Site.objects.get_current()
        query_param = 'site:%s %s' % (site.domain, search_query)
        params = {
            'v': '1.0',
            'rsz': 'large',
            'start': (page - 1) * 8,
            'q': query_param,
        }
        base_search_url = 'http://www.google.com/uds/GwebSearch'
        search_url = '?'.join([base_search_url,
            urllib.urlencode(params.items())])
        # Build a request and get the JSON search results from Google.
        search_request = urllib2.Request(search_url)
        search_request.add_header('User-Agent', '%s (%s)' % (site.name,
            site.domain))
        opener = urllib2.build_opener()
        # Get all the useful 
        try:
            json = simplejson.loads(opener.open(search_request).read())
            raw_search_results = json['responseData']['results']
            total_pages = len(json['responseData']['cursor']['pages'])
            current_page = json['responseData']['cursor']['currentPageIndex'] + 1
            next_page = current_page + 1 if current_page != total_pages else False
            previous_page = current_page - 1 if current_page > 1 else False
        except urllib2.HTTPError, AttributeError:
            raw_search_results = {}
        # Loop through each result and strip ' — Flother' from the titles.
        for result in raw_search_results:
            title = result['titleNoFormatting'].rsplit(u'—', 1)[0].strip()
            search_results.append({'title': title, 'url': result['url'],
                'content': result['content']})
    context = {
        'search_query': search_query,
        'search_results': search_results,
        'first_result': ((page - 1) * 8) + 1,
        'total_pages': total_pages,
        'current_page': current_page,
        'next_page': next_page,
        'previous_page': previous_page,
    }
    return render_to_response('search/search_results.html', context,
        context_instance=RequestContext(request))
