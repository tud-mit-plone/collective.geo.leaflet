var overlayers = {};
urls = $('#geojson_url').data('geojson_url');
var geojsons = [];
for (u in urls) {
    url = urls[u];
    var layername;
    $.getJSON(url, function(data) {
        layername = data.title;
        geojson = L.geoJson(data, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(
                    '<a href="'+feature.properties.url+'" target="_blank">'+
                    '<h3>'+feature.properties.title+'</h3>'+
                    '</a>'+
                    '<p>'+feature.properties.description+'</p>');
            },
            pointToLayer: function (feature, latlng) {
                //Extend the Default marker class
                var CustomIcon = L.Icon.Default.extend({
                    options: {
                        iconUrl: feature.style.image
                    }
                });
                var customIcon = new CustomIcon();
                return L.marker(latlng, {icon: customIcon});
            }
        }).addTo(map);
        controllayers.addOverlay(geojson, layername);
        //overlayers[layername] = geojson;
    });
}

controllayers.addTo(map);
