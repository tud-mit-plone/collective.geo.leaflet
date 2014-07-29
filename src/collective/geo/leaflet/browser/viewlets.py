# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.mapwidget.utils import get_feature_styles

from collective.geo.leaflet.interfaces import IMapLayer
from collective.geo.leaflet import utils

from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.settings.interfaces import IGeoSettings

from plone import api
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.Expression import Expression, getExprContext

from zope.schema import getFields
from zope.component import getMultiAdapter
from zope.component import getUtility
import logging
logger = logging.getLogger("collective.geo.leaflet")


class ContentViewlet(common.ViewletBase):

    index = ViewPageTemplateFile('templates/leafletcontentviewlet.pt')

    @property
    def coordinates(self):
        view = getMultiAdapter((self.context, self.request), name="geoview")
        return view.getCoordinates()

    @property
    def map_viewlet_position(self):
        styles = get_feature_styles(self.context)
        if styles.get('use_custom_styles', False):
            return styles.get('map_viewlet_position')
        else:
            return api.portal.get_registry_record(
                'collective.geo.settings.interfaces.IGeoFeatureStyle.map_viewlet_position')

    def render(self):
        if self.manager.__name__ != self.map_viewlet_position:
            return ''

        type, coords = self.coordinates
        if type and coords:
            return super(ContentViewlet, self).render()
        else:
            return ''

    def map_infos(self):
        return utils.get_geo_infos(self.context)

    def style(self):
        infos = utils.get_geo_infos(self.context)
        style = []
        if infos.get('map_height'):
            style.append('height: {}'.format(infos.get('map_height')))
        else:
            style.append('height: 600px')
        if infos.get('map_width'):
            style.append("width: {}".format(infos.get('map_width')))
        else:
            style.append("width: 800px")
        return ";".join(style)

    def make_popup(self):
        # XXX should be in a template
        popup = "<div class='geo-popup'>"
        geo_infos = utils.get_geo_infos(self.context)
        for prop in geo_infos.get('display_properties', []):
            popup += getattr(self.context, prop)()
            popup += '<br />'
        popup += "</div>"
        return popup

    def default_layers(self):
        return utils.default_layers(self.context, self.request)
