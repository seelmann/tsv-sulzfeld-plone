#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import numbers
from zope import interface
from collective.easytemplate.engine import getEngine, getTemplateContext 
from collective.templateengines.interfaces import ITag
from collective.templateengines.utils import DictionaryContext
from DateTime import DateTime



class TodayTag(object):
    
    interface.implements(ITag)
    
    def getName(self):
        return "today"
    
    def render(self, scriptingContext):
        locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
        return DateTime().earliestTime()


class VereinstermineTag(object):

    interface.implements(ITag)
    
    def getName(self):
        return "vereinstermine"

    def render(self, scriptingContext, anzahl=1000, start=None, ende=None):
        mappings = scriptingContext.getMappings()
        context = mappings["context"]
        dateQuery = getDateQuery(start, ende)
        items = context.portal_catalog.queryCatalog({
            "portal_type":"vereinstermin",
            "review_state":"published",
            "start":dateQuery,
            "sort_on":"start",
            "sort_limit":anzahl,
        })
        scriptingContext.addMapping("items", items)
        result = render(self.template, scriptingContext)
        return result

    template = """
<table class="plain">
<tbody>
<tr><th>Wann</th><th>Wo</th><th>Was</th><th>Beschreibung</th>{% if not portal_state.anonymous() %}<th></th>{% endif %}</tr>
{% for item in items %}
<tr>
<td>{{ item.getObject().start.strftime("%A, %d. %B %Y um %H:%M") }}</td>
<td>{{ item.getObject().location }}</td>
<td>{{ item.getObject().title }}</td>
<td>{{ item.getObject().description }}</td>
{% if not portal_state.anonymous() %}
<td><a href="{{ item.getPath() }}/edit">bearbeiten</a></td>
{% endif %}
</tr>
{% endfor %}
</tbody>
</table>
"""


class SpieltermineTag(object):

    interface.implements(ITag)
    
    def getName(self):
        return "spieltermine"

    def render(self, scriptingContext, anzahl=1000, sportart=None, spielart=None, mannschaft=None, start=None, ende=None, felder=[]):

        mappings = scriptingContext.getMappings()
        context = mappings["context"]
        dateQuery = getDateQuery(start, ende)
        results = context.portal_catalog.queryCatalog({
            "portal_type":"spieltermin",
            "review_state":"published",
            "sportart":sportart,
            "mannschaft":mannschaft,
            "spielart":spielart,
            "start":dateQuery,
            "sort_on":"start",
            #"sort_order":"reverse",
            "sort_limit":anzahl,
        })

        items = []
        for item in results:
            obj = item.getObject()
            fields = {
                "sportart":obj.sportart,
                "mannschaft":obj.mannschaft,
                "spielart":obj.spielart,
                "datum":obj.start.strftime("%A, %d. %B %Y um %H:%M"),
                "heim":obj.heim,
                "gast":obj.gast,
                "ergebnis":obj.ergebnis or "",
                "details":'<a href="%s" class="link-overlay">Details</a>' % item.getPath(),
                "edit":'<a href="%s/edit">bearbeiten</a>' % item.getPath(), 
            }
            items.append(fields)
        
        if not mappings["portal_state"].anonymous():
            felder.append("edit")
        
        scriptingContext.addMapping("felder", felder)
        scriptingContext.addMapping("headers", self.headers)
        scriptingContext.addMapping("items", items)
        result = render(self.template, scriptingContext)

        return result


    headers = {
        "sportart":"Sportart",
        "mannschaft":"Mannschaft",
        "spielart":"Spielart",
        "datum":"Wann",
        "heim":"Heim",
        "gast":"Gast",
        "ergebnis":"Ergebnis",
        "details":"",
        "edit":"", 
    }

    template = """
<table class="plain">
<tbody>
<tr>
{% for feld in felder %}
<th>{{ headers[feld] }}</th>
{% endfor %}
</tr>
{% for item in items %}
<tr>
{% for feld in felder %}
<td>{{ item[feld] }}</td>
{% endfor %}
</tr>
{% endfor %}
</tbody>
</table>
    """

def getDate(offset, default):
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    if offset is not None:
        if isinstance(offset, numbers.Number):
            return DateTime().earliestTime() + offset 
        else:
            return DateTime(offset)
    return default

def getDateQuery(start, end):
    startDate = getDate(start, DateTime().earliestTime())
    endDate = getDate(end, None)
    if endDate is not None:
        dateQuery = {"query":(startDate,endDate), "range":"min:max"}
    else:
        dateQuery = {"query":startDate, "range":"min"}
    return dateQuery

def render(template, scriptingContext):
    engine = getEngine()
    template, errors = engine.loadString(template, False)
    result, evaluation_errors = template.evaluate(scriptingContext)
    return result

