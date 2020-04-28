.. contents::

==========================================================================
collective.geo.leaflet
==========================================================================

This package use the collective.geo.* suite with leaflet.


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


Translations
============

This product has been translated into

- Spanish.

- French.

- Dutch.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
============

Install collective.geo.leaflet by adding it to your buildout:

   [buildout]

    ...

    eggs =
        collective.geo.leaflet


and then running "bin/buildout"


Dependencies
------------

- collective.geo.behaviour
- collective.geo.contentlocations
- collective.geo.geographer
- collective.geo.json
- collective.geo.mapwidget
- collective.geo.openlayers
- collective.geo.settings
- collective.js.leaflet
- collective.z3cform.mapwidget
- collective.z3cform.colorpicker


How to add baseLayer
====================

What is a leaflet baseLayer :
http://leafletjs.com/examples/layers-control.html


In Plone, if you want to add a baseLayer, you have to add a subscriber on collective.geo.geographer.interfaces.IGeoreferenced (for exemple, in `configure.zcml`)::

    <subscriber
        for="collective.geo.geographer.interfaces.IGeoreferenced"
        provides="collective.geo.leaflet.interfaces.IMapLayer"
        factory=".maplayers.OpenStreetMap
        />

After, create your factory in python (`maplayers.py`)::

    from collective.geo.leaflet.maplayers import MapLayer
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


    class OpenStreetMap(MapLayer):
        name = u"osm"
        title = _(u"Open Street Map")
        index = ViewPageTemplateFile('browser/layers/osm.pt')

And add your javascript into a template file `osm.pt`::

    <script type="text/javascript">
        var osmAttrib = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
        var osmUrl = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png';
        var %(name)s = L.tileLayer(osmUrl, {
             attribution: osmAttrib,
        });
    </script>


Todo
====

[ ] Get "attribution" map from registry

[ ] Testing loading map with Robot

[x] Add uninstall profile

[x] Translations

[ ] Simple element view should use geojson

[ ] Use leaflet for control panel map

[ ] Use leaflet for configure map


Tests status
============

This package is tested using Travis CI. The current status is :

.. image:: https://img.shields.io/travis/collective/collective.geo.leaflet/master.svg
    :target: https://travis-ci.org/collective/collective.geo.leaflet

.. image:: http://img.shields.io/pypi/v/collective.geo.leaflet.svg
   :target: https://pypi.org/project/collective.geo.leaflet


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.leaflet/issues
- Source Code: https://github.com/collective/collective.geo.leaflet
- Documentation: https://collectivegeo.readthedocs.io/


License
=======

The project is licensed under the GPLv2.

.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
