var sidebar = L.Control.extend({
    options: {
        position: 'bottomright'
    },
    onAdd: function (map) {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
        container.style.backgroundColor = "white";
        container.style.height = '600px';
        container.style.width = '400px';
        /*
         var button = document.createElement("button");
         button.textContent = "Topliste";
         container.appendChild(button);
         */

        var table = L.DomUtil.create("table", "sidebarTable pure-table pure-table-horizontal", container);

        console.log($(container));
        $(container).pagination({
            dataSource: "/api/top/",
            locator: 'items',
            totalNumber: 121, //14400
            pageSize: 10,
            position: 'top',
            ajax: {
                data: {type: "farAway"},
                cache: true,
                beforeSend: function (a) {
                    // dataContainer.html('Loading data from flickr.com ...');
                }
            },
            callback: function (data, pagination) {
                console.log(pagination);
                while (table.firstChild) {
                    table.removeChild(table.firstChild);
                }
                for (var i = 0; i < data.length; i++) {
                    var line = document.createElement("tr");
                    var single = data[i];
                    for (var j = 0; j < single.length; j++) {
                        var td = document.createElement("td");
                        td.textContent = single[j];
                        line.appendChild(td);
                    }
                    table.appendChild(line);
                }
            }
        });

        return container;
    }
});
map.addControl(new sidebar);

function loadSidebar(table) {
    $.getJSON("/api/top/", {
        type: "shortestConnections"
    }).done(function (data) {
        while (table.firstChild) {
            table.removeChild(table.firstChild);
        }
        for (var i = 0; i < data.length; i++) {
            var line = document.createElement("tr");
            var single = data[i];
            for (var j = 0; j < single.length; j++) {
                var td = document.createElement("td");
                td.textContent = single[j];
                line.appendChild(td);
            }
            table.appendChild(line);
        }
    });

}