# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common

from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.geographer.interfaces import IGeoreferenceable

from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.utils import get_feature_styles

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

from zope.schema import getFields
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoFeatureStyle


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
        if not IGeoreferenceable.providedBy(self.context):
            return ""
        if self.manager.__name__ != self.map_viewlet_position:
            return ''

        type, coords = self.coordinates
        if type and coords:
            return super(ContentViewlet, self).render()
        else:
            return ''

    def map_infos(self):
        return get_geo_infos(self.context)

    def style(self):
        infos = get_geo_infos(self.context)
        style = []
        if infos.get('map_height'):
            style.append('height: {}'.format(infos.get('map_height')))
        if infos.get('map_width'):
            style.append("width: {}".format(infos.get('map_width')))
        return ";".join(style)

    def make_popup(self):
        popup = "<div class='geo-popup'>"
        geo_infos = get_geo_infos(self.context)
        for prop in geo_infos.get('display_properties', []):
            popup += self.context.get(prop)
        popup += "</div>"
        return popup



class LeafletMapViewletLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(LeafletMapViewletLayers, self).layers()
        return layers


def get_geo_infos(context):
    if not IGeoreferenceable.providedBy(context):
        return ""
    fields = [i for i in getFields(IGeoFeatureStyle)]
    manager = IGeoFeatureStyle(context, None)
    if not manager:
        return False
    use_custom_styles = getattr(manager, 'use_custom_styles', False)
    if not use_custom_styles:
        registry = getUtility(IRegistry)
        manager = registry.forInterface(IGeoFeatureStyle)

    styles = {
        'use_custom_styles': use_custom_styles
    }
    for name in fields:
        styles[name] = getattr(manager, name, None)

    geo = IGeoreferenced(context)
    styles['longitude'] = geo.coordinates[0]
    styles['latitude'] = geo.coordinates[1]
    return styles
