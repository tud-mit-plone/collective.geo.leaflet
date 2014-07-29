# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.geo.leaflet import utils


class GeoLeaflet(BrowserView):

    index = ViewPageTemplateFile("templates/geo-leaflet.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def map_infos(self):
        return utils.get_geo_infos(self.context)

    def make_popup(self):
        # XXX should be in a template
        popup = "<div class='geo-popup'>"
        geo_infos = utils.get_geo_infos(self.context)
        for prop in geo_infos.get('display_properties', []):
            popup += getattr(self.context, prop)()
            popup += '<br />'
        popup += "</div>"
        return popup

