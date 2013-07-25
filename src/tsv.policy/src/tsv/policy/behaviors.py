from tsv.policy.interfaces import INameForSpieltermin
from zope import interface
from datetime import timedelta
from plone.app.content.interfaces import INameFromTitle

class INameForSpieltermin(INameFromTitle):

    def title():
        """Titel fuer Spieltermin"""

class NameForSpieltermin(object):
    interface.implements(INameForSpieltermin)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        date = self.context.start - timedelta(days=180)
        year = date.strftime("%Y")
        return u"%s %s %s" % (year, self.context.heim, self.context.gast)

