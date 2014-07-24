# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.mapwidget.utils import get_feature_styles

from collective.geo.leaflet.interfaces import IMapLayer

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
from zope.component import getGlobalSiteManager
import json
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
        return get_geo_infos(self.context)

    def style(self):
        infos = get_geo_infos(self.context)
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
        geo_infos = get_geo_infos(self.context)
        for prop in geo_infos.get('display_properties', []):
            popup += getattr(self.context, prop)()
            popup += '<br />'
        popup += "</div>"
        return popup

    def default_layers(self):
        registred_layers = {}
        ordered_layers = []
        baselayers = []

        gsm = getGlobalSiteManager()
        for registration in gsm.registeredSubscriptionAdapters():
            if registration.provided is IMapLayer:
                layer = registration.factory(self.context, self.request)
                registred_layers[layer.name] = layer

        geosettings = getUtility(IRegistry).forInterface(IGeoSettings)
        default_layers = geosettings.default_layers
        if not default_layers:
            default_layers = (u'osm',)

        for default_layer in default_layers:
            if default_layer in registred_layers.keys():
                l = registred_layers[default_layer]
                baselayers.append({"title": l.title, "name": l.name})
                ordered_layers.append(l.index() % dict(name=l.name))

        return {
            "layers": "\n".join(ordered_layers),
            "baselayers": json.dumps(baselayers)
        }


def get_marker_image(context, marker_img):
    try:
        marker_img = Expression(str(marker_img))(getExprContext(context))
    except:
        marker_img = ''
    return marker_img


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
    styles['marker_image'] = get_marker_image(context, styles['marker_image'])
    return styles
