var baselayers = {};
var overlayMaps = {};
var map;
var longitude = $('#map').data('longitude');
var latitude = $('#map').data('latitude');
var marker_url = $('#map').data('marker_image');
map = new L.Map('map').setView([latitude, longitude], 13);

$(document).ready(function() {

    var tiles = new L.TileLayer(
        'http://mt{s}.google.com/vt/v=w2.106&x={x}&y={y}&z={z}&s=',
        { subdomains:'0123', attribution:'&copy; Google 2012' }
    );
    //osm.addTo(map);
    /*baseMaps['osm'] = osm;
    baseMaps['google roadmap'] = googleroad;
    baseMaps['google satelite'] = googlesat;
    baseMaps['google terrain'] = googleterrain;
    baseMaps['google hybrid'] = googlehybrid;
    baseMaps['tiles'] = tiles;
    */

});
