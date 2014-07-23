# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.geo.leaflet.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of collective.geo.leaflet into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.geo.leaflet is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.geo.leaflet'))

    def test_uninstall(self):
        """Test if collective.geo.leaflet is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.geo.leaflet'])
        self.assertFalse(self.installer.isProductInstalled('collective.geo.leaflet'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveGeoLeafletLayer is registered."""
        from collective.geo.leaflet.interfaces import ICollectiveGeoLeafletLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveGeoLeafletLayer, utils.registered_layers())
