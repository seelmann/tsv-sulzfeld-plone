from  tsv.theme.testing import TSV_THEME_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_test.txt"),
                layer=TSV_THEME_FUNCTIONAL_TESTING)
    ])
    return suite