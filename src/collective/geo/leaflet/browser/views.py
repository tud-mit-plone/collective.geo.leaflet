# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.geo.leaflet import geomap
from zope.component import getMultiAdapter
import json


class GeoLeaflet(BrowserView):

    index = ViewPageTemplateFile("templates/geo-leaflet.pt")

    def __init__(self, context, request):
        super(GeoLeaflet, self).__init__(context, request)
        self.geomap = geomap.GeoMap(context, request)

    def __call__(self):
        return self.render()

    def render(self):
         return self.index()

    def make_popup(self):
        # XXX should be in a template
        popup = "<div class='geo-popup'>"
        geo_infos = utils.get_geo_infos(self.context)
        for prop in geo_infos.get('display_properties', []):
            popup += getattr(self.context, prop)()
            popup += '<br />'
        popup += "</div>"
        return popup

    def geojson_urls(self):
        return json.dumps(["{}/@@geo-json.json".format(self.context.absolute_url())])

    def geojson(self):
        return getMultiAdapter((self.context, self.request), name="geo-json.json")
