var sidebar = L.Control.extend({
    options: {
        position: 'bottomright'
    },
    onAdd: function (map) {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
        container.style.backgroundColor = "white";
        container.style.height = '600px';
        container.style.width = '400px';
        var table = L.DomUtil.create("table", "sidebarTable", container);
        var button = document.createElement("button");
        button.textContent = "Topliste";
        container.appendChild(button);

        return container;
    }
});
map.addControl(new sidebar);

$(".leaflet-control-custom button").on("click", function () {
    loadSidebar();
});

function loadSidebar() {
    $.getJSON("/api/top/", {
        type: "shortestConnections"
    }).done(function (data) {
        var table = $(".sidebarTable");
        for (var i = 0; i < data.length; i++) {
            var line = document.createElement("tr");
            var single = data[i];
            console.log(single);
            for (var j = 0; j < single.length; j++) {
                var td = document.createElement("td");
                td.textContent = single[j];
                line.appendChild(td);
            }
            table.append(line);
        }

    });

}