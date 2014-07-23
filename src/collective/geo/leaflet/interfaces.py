# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveGeoLeafletLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ILeafletViewlet(Interface):
    """Marker interface for Viewlet """
