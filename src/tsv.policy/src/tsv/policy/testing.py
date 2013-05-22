from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class TsvpolicyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import tsv.policy
        xmlconfig.file(
            'configure.zcml',
            tsv.policy,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')


TSV_POLICY_FIXTURE = TsvpolicyLayer()
TSV_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TSV_POLICY_FIXTURE,),
    name="TsvpolicyLayer:Integration"
)
TSV_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TSV_POLICY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="TsvpolicyLayer:Functional"
)
