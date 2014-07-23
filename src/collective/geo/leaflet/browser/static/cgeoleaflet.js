$(document).ready(function() {
    if ($('#map').length === 0) {
        return;
    }


    var longitude = $('#map').data('longitude');
    var latitude = $('#map').data('latitude');
    var marker_url = $('#map').data('marker_image');

    var map = new L.Map('map').setView([latitude, longitude], 13);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    //map.locate({setView: true});
    var markercoord = [latitude, longitude];

    //Extend the Default marker class
    var CustomIcon = L.Icon.Default.extend({
        options: {
            iconUrl: 'img/marker.png', //marker_url
        }
    });

    var customIcon = new CustomIcon();

    var marker = L.marker(markercoord, {icon: customIcon}).addTo(map);

    // XXX gettext via json
    marker.bindPopup('text');

    new L.Control.GeoSearch({
        provider: new L.GeoSearch.Provider.OpenStreetMap(),
        position: 'topcenter',
        showMarker: true
    }).addTo(map);
});
