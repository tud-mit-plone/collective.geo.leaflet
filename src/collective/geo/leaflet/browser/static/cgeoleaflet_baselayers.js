var controllayers;
baselayers = {};
layers = $('div.baselayers').data('baselayers');
for (var layer in layers) {
    baselayers[layers[layer].title] = eval(layers[layer].name);
}
eval(layers[0].name).addTo(map);
controllayers = L.control.layers(baselayers);
