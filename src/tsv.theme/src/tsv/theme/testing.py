from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class TsvthemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import tsv.theme
        xmlconfig.file(
            'configure.zcml',
            tsv.theme,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tsv.theme:default')

TSV_THEME_FIXTURE = TsvthemeLayer()
TSV_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TSV_THEME_FIXTURE,),
    name="TsvthemeLayer:Integration"
)
TSV_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TSV_THEME_FIXTURE, z2.ZSERVER_FIXTURE),
    name="TsvthemeLayer:Functional"
)
