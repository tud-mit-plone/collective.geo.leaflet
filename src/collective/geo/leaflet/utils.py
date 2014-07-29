# -*- coding: utf-8 -*-
from collective.geo.geographer.interfaces import IGeoreferenceable
from collective.geo.geographer.interfaces import IGeoreferenced

from collective.geo.leaflet.interfaces import IMapLayer

from collective.geo.settings.interfaces import IGeoFeatureStyle
from collective.geo.settings.interfaces import IGeoSettings

from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import Expression, getExprContext
from zope.schema import getFields
from zope.component import getUtility
from zope.component import getGlobalSiteManager
import json


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


def get_marker_image(context, marker_img):
    try:
        marker_img = Expression(str(marker_img))(getExprContext(context))
    except:
        marker_img = ''
    return marker_img


def default_layers(context, request):
        registred_layers = {}
        ordered_layers = []
        baselayers = []

        gsm = getGlobalSiteManager()
        for registration in gsm.registeredSubscriptionAdapters():
            if registration.provided is IMapLayer:
                layer = registration.factory(context, request)
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
