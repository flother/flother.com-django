# -*- coding: utf-8 -*-

"""Python wrapper for geoname web APIs

created 19/03/2006 By Nicolas Laurance

This module allows you to access geoname's web APIs,
and get the results programmatically.
Described here:
  http://www.geonames.org/export/

It is based on the Mark Pilgrim's technorati API :
  http://www.sifry.com/alerts/archives/000288.html

def postalCodeSearch(postalcode, placename='', country=COUNTRY, maxRows='10', http_proxy=None):
def postalCodeLookupJSON(postalcode, placename='', country=COUNTRY, maxRows='10',gcallback='', http_proxy=None):
def findNearbyPostalCodes(postalcode, placename='', country=COUNTRY, radius='5', maxRows='10',lat=None,lng=None, http_proxy=None):
def postalCodeCountryInfo(http_proxy=None):
def search(placename='', country=COUNTRY, maxRows='10', style='SHORT',lang=LANG, fclass=None, http_proxy=None):
def findNearbyPlaceName(lat,lng, http_proxy=None):

Sample usage:
>>> import geoname
>>> result=geoname.postalCodeSearch('35580','guichen','fr','10')
>>> result.totalResultsCount
1
>>> result.code[0].lat
47.966666699999998
>>> result.code[0].lng
-1.8

>>> result=geoname.postalCodeLookupJSON('35580','guichen','fr','10')
>>> result['postalcodes']
[{'postalcode': '35580', 'placeName': 'Guichen', 'countryCode': 'FR'}]

>>> result=geoname.findNearbyPostalCodes('35000','rennes','FR',10,10)
>>> for b in result.code:
...     print '%s : %s' %(b.name,b.postalcode)
...
Rennes : 35700
Rennes : 35200
Rennes : 35000
St Jacques De La Lande : 35136
Noyal Sur Seiche : 35230
Pont Pean : 35131
Chartres De Bretagne : 35131
Chantepie : 35135
Chatillon Sur Seiche : 35230
St Gregoire : 35760

>>> result=geoname.findNearbyPostalCodes('','','FR',10,10,47.97,-1.8)
>>> for b in result.code:
...      print '%s : %s' %(b.name,b.postalcode)
...
Guichen : 35580
Pont Rean : 35580
Pont Rean : 35170
Goven : 35580
Lassy : 35580
Bourg Des Comptes : 35890
Guignen : 35580
St Senoux : 35580
Bruz : 35170
Chavagne : 35310


>>> result=geoname.search('guichen','fr',5,'SHORT','fr')
>>> result.totalResultsCount
3
>>> for b in result.geoname:
...     print '%s' %(b.name)
...
Guichen
Guiche
La Guiche


>>> result=geoname.findNearbyPlaceName(47.97,-1.8)
>>> for b in result.geoname:
...     print '%s' % b.name
...
Guichen

"""

__author__ = "Nicolas Laurance (nlaurance@zindep.com)"
__version__ = "0.1"
__cvsversion__ = "$Revision: 1.0 $"[11:-2]
__date__ = "$Date: 2003/06/19 22:40:53 $"[7:-2]
__copyright__ = "Copyright (c) 2006 Nicolas Laurance"
__license__ = "Python"

from xml.dom import minidom
import os, sys, urllib, re
try:
    import timeoutsocket # http://www.timo-tasi.org/python/timeoutsocket.py
    timeoutsocket.setDefaultSocketTimeout(120)
except ImportError:
    pass

HTTP_PROXY = None
DEBUG = 0
COUNTRY = 'FR'
LANG ='fr'


# don't touch the rest of these constants
class GeonameError(Exception): pass

## administrative functions
def version():
    print """PyGeoname %(__version__)s
%(__copyright__)s
released %(__date__)s
""" % globals()

def setProxy(http_proxy):
    """set HTTP proxy"""
    global HTTP_PROXY
    HTTP_PROXY = http_proxy

def getProxy(http_proxy = None):
    """get HTTP proxy"""
    return http_proxy or HTTP_PROXY

def getProxies(http_proxy = None):
    http_proxy = getProxy(http_proxy)
    if http_proxy:
        proxies = {"http": http_proxy}
    else:
        proxies = None
    return proxies

def _contentsOf(dirname, filename):
    filename = os.path.join(dirname, filename)
    if not os.path.exists(filename): return None
    fsock = open(filename)
    contents = fsock.read()
    fsock.close()
    return contents

def _getScriptDir():
    if __name__ == '__main__':
        return os.path.abspath(os.path.dirname(sys.argv[0]))
    else:
        return os.path.abspath(os.path.dirname(sys.modules[__name__].__file__))

class Bag: pass

_intFields = ('totalResultsCount')
_dateFields = ()
_listFields = ('code','geoname','country',)
_floatFields = ('lat','lng','distance')

def unmarshal(element):
    #import pdb;pdb.set_trace()
    rc = Bag()
    childElements = [e for e in element.childNodes if isinstance(e, minidom.Element)]
    if childElements:
        for child in childElements:
            key = child.tagName
            if hasattr(rc, key):
                if key in _listFields:
                    setattr(rc, key, getattr(rc, key) + [unmarshal(child)])
            elif isinstance(child, minidom.Element) and (child.tagName in ( )):
                rc = unmarshal(child)
            elif key in _listFields:
                setattr(rc, key, [unmarshal(child)])
            else:
                setattr(rc, key, unmarshal(child))
    else:
        rc = "".join([e.data for e in element.childNodes if isinstance(e, minidom.Text)])
        if str(element.tagName) in _intFields:
            rc = int(rc)
            if DEBUG: print '%s : %s' % (element.tagName,rc)
        elif str(element.tagName) in _floatFields:
            rc = float(rc)
            if DEBUG: print '%s : %s' % (element.tagName,rc)
        elif str(element.tagName) in _dateFields:
            year, month, day, hour, minute, second = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', rc).groups()
            rc = (int(year), int(month), int(day), int(hour), int(minute), int(second), 0, 0, 0)
            if DEBUG: print '%s : %s' % (element.tagName,rc)
    return rc

def _do(url, http_proxy):
    proxies = getProxies(http_proxy)
    u = urllib.FancyURLopener(proxies)
    usock = u.open(url)
    rawdata = usock.read()
    if DEBUG: print rawdata
    xmldoc = minidom.parseString(rawdata)
    usock.close()
    data = unmarshal(xmldoc)
#    if hasattr(data, 'ErrorMsg'):
    if 0:
        raise TechnoratiError, data
    else:
        return data

## main functions

def _buildfindNearbyPostalCodes(postalcode, placename, country, radius, maxRows ):
    placename=urllib.quote(placename)
    searchUrl = "http://ws.geonames.org/findNearbyPostalCodes?postalcode=%(postalcode)s&placename=%(placename)s&country=%(country)s&radius=%(radius)s&maxRows=%(maxRows)s" % vars()
    return searchUrl


def _buildpostalCodeLookupJSON(postalcode,placename,country,maxRows,gcallback):
    placename=urllib.quote(placename)
    searchUrl = "http://ws.geonames.org/postalCodeLookupJSON?postalcode=%(postalcode)s&placename=%(placename)s&country=%(country)s&maxRows=%(maxRows)s&callback=%(gcallback)s" % vars()
    return searchUrl

def _buildfindNearbyPostalCodesLL(lat,lng,radius,maxRows):
    searchUrl = "http://ws.geonames.org/findNearbyPostalCodes?lat=%(lat)s&lng=%(lng)s&radius=%(radius)s&maxRows=%(maxRows)s" % vars()
    return searchUrl

def _buildfindNearbyPlaceName(lat,lng):
    searchUrl = "http://ws.geonames.org/findNearbyPlaceName?lat=%(lat)s&lng=%(lng)s" % vars()
    return searchUrl

def _buildpostalCodeSearch(postalcode, placename, country, maxRows ):
    placename=urllib.quote(placename)
    searchUrl = "http://ws.geonames.org/postalCodeSearch?postalcode=%(postalcode)s&placename=%(placename)s&country=%(country)s&maxRows=%(maxRows)s" % vars()
    return searchUrl

def _buildsearch(placename, country, maxRows,style,lang, fclass):
    placename=urllib.quote(placename)
    if fclass:
        urlfclass=''
        for fc in fclass:
            urlfclass+=urllib.quote("&fclass=%s" % fc)
    searchUrl = "http://ws.geonames.org/search?q=%(placename)s&country=%(country)s&maxRows=%(maxRows)s&lang=%(lang)s&style=%(style)s&fclass=%(fclass)s" % vars()
    return searchUrl

def postalCodeSearch(postalcode, placename='', country=COUNTRY, maxRows='10', http_proxy=None):
    """
    http://ws.geonames.org/postalCodeSearch?postalcode=35580&maxRows=10&country=fr
    Url : ws.geonames.org/postalCodeSearch?
    Parameters : postalcode ,placename,maxRows,country
    <geonames>
    <totalResultsCount>7</totalResultsCount>
    -
    <code>
        <postalcode>35580</postalcode>
        <name>St Senoux</name>
        <countryCode>FR</countryCode>
        <lat>47.9</lat>
        <lng>-1.7833333</lng>
    </code>
    """
    url = _buildpostalCodeSearch(postalcode,placename,country,maxRows)
    if DEBUG: print url
    return _do(url,http_proxy).geonames

def postalCodeLookupJSON(postalcode, placename='', country=COUNTRY, maxRows='10',gcallback='', http_proxy=None):
    """
    Webservice Type : REST /JSON
    Url : ws.geonames.org/postalCodeLookupJSON?
    Parameters : postalcode,country ,maxRows (default = 20),callback
    Result : returns a list of places for the given postalcode in JSON format
    """
    url = _buildpostalCodeLookupJSON(postalcode,placename,country,maxRows,gcallback)
#    print url
    proxies = getProxies(http_proxy)
    u = urllib.FancyURLopener(proxies)
    usock = u.open(url)
    rawdata = usock.read()
    if DEBUG: print rawdata
    usock.close()
    return eval(rawdata[:-3])

def findNearbyPostalCodes(postalcode, placename='', country=COUNTRY, radius='5', maxRows='10',lat=None,lng=None, http_proxy=None):
    """
    Find nearby postal codes / reverse geocoding
    This service comes in two flavors. You can either pass the lat/long or a postalcode/placename.

    Webservice Type : REST
    Url : ws.geonames.org/findNearbyPostalCodes?
    Parameters :
    lat,lng, radius (in km), maxRows (default = 5),country (default = all countries)
    or
    postalcode,country, radius (in Km), maxRows (default = 5)
    Result : returns a list of postalcodes and places for the lat/lng query as xml document
    Example: 
    http://ws.geonames.org/findNearbyPostalCodes?postalcode=35580&placename=guichen&country=FR&radius=5
    <geonames>
    -
    <code>
        <postalcode>35580</postalcode>
        <name>Guichen</name>
        <countryCode>FR</countryCode>
        <lat>47.9666667</lat>
        <lng>-1.8</lng>
        <distance>0.0</distance>
    </code>
    """
    if lat and lng :
        url = _buildfindNearbyPostalCodesLL(lat,lng,radius,maxRows)
    else:
        url = _buildfindNearbyPostalCodes(postalcode,placename,country,radius,maxRows)
    if DEBUG: print url
#    import pdb;pdb.set_trace()
    return _do(url,http_proxy).geonames


def postalCodeCountryInfo(http_proxy=None):
    """
    http://ws.geonames.org/postalCodeCountryInfo?
    <country>
    <countryCode>FR</countryCode>
    <countryName>France</countryName>
    <numPostalCodes>39163</numPostalCodes>
    <minPostalCode>01000</minPostalCode>
    <maxPostalCode>98000</maxPostalCode>
    </country>

    """
    return _do("http://ws.geonames.org/postalCodeCountryInfo?",http_proxy).geonames.country

def search(placename='', country=COUNTRY, maxRows='10', style='SHORT',lang=LANG, fclass=None, http_proxy=None):
    """
    Url : ws.geonames.org/search?
    Parameters : 	q : place name (urlencoded utf8)
    maxRows : maximal number of rows returned (default = 100)
    country : iso country code, two characters (default = all countries)
    fclass : featureclass(es) (default= all feature classes); this parameter may occur more then once, example: fclass=P&fclass=A
    style : SHORT,MEDIUM,LONG (default = MEDIUM), verbosity of returned xml document
    lang : ISO 2-letter language code. (default = en), countryName will be returned in the specified language. 

    http://ws.geonames.org/search?q=guichen&maxRows=10&style=SHORT&lang=fr&country=fr
        <geonames>
        <totalResultsCount>3</totalResultsCount>
        -
        <geoname>
            <name>Laillé</name>
            <lat>47.9833333</lat>
            <lng>-1.7166667</lng>
        </geoname>
    """
    url = _buildsearch(placename, country, maxRows,style,lang, fclass)
    if DEBUG: print url
    return _do(url,http_proxy).geonames

def findNearbyPlaceName(lat,lng, http_proxy=None):
    """
    Webservice Type : REST
    Url : ws.geonames.org/findNearbyPlaceName?
    Parameters : lat,lng
    Result : returns the closest populated place for the lat/lng query as xml document
    Example:
    http://ws.geonames.org/findNearbyPlaceName?lat=47.3&lng=9     
    """
    url = _buildfindNearbyPlaceName(lat,lng)
    if DEBUG: print url
    return _do(url,http_proxy).geonames

