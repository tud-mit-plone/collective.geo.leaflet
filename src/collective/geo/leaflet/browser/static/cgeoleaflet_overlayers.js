var overlayers = {};
urls = $('#geojson_url').data('geojson_url');
for (u in urls) {
    url = urls[u];
    var geojson;
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
        });
        overlayers[layername] = geojson;
    });
}
