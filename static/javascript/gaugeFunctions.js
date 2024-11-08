// Define options globally
var methoptions = {
    min: 0, max: 10000,
    width: 400, height: 140,
    redFrom: 8000, redTo: 10000,
    yellowFrom: 1000, yellowTo: 8000,
    minorTicks: 20
};

var carboptions = {
    min: 0, max: 1000,
    width: 400, height: 140,
    redFrom: 500, redTo: 1000,
    yellowFrom: 50, yellowTo: 500,
    minorTicks: 20
};

var aqoptions = {
    min: 0, max: 1000,
    width: 400, height: 140,
    redFrom: 700, redTo: 1000,
    yellowFrom: 200, yellowTo: 700,
    minorTicks: 20
};

var butoptions = {
    min: 0, max: 1600,
    width: 400, height: 140,
    redFrom: 1000, redTo: 1600,
    yellowFrom: 700, yellowTo: 1000,
    minorTicks: 30
};

google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var methdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Methane', 0]
    ]);
    var carbondata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['CO', 0]
    ]);
    var aqdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Air Quality', 0]
    ]);
    var butdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Butane', 0]
    ]);

    var methguage = new google.visualization.Gauge(document.getElementById('methaneGauge'));
    var carbguage = new google.visualization.Gauge(document.getElementById('carbonGauge'));
    var aqguage = new google.visualization.Gauge(document.getElementById('aqGauge'));
    var butguage = new google.visualization.Gauge(document.getElementById('butaneGauge'));

    methguage.draw(methdata, methoptions);
    carbguage.draw(carbondata, carboptions);
    aqguage.draw(aqdata, aqoptions);
    butguage.draw(butdata, butoptions);
}

function sendGuageUpdate() {
    $.post("/getGaugeData", {}, function(data){
        updateGuages(data);
    });
}

function updateGuages(data) {
    // Create new data tables for each gauge
    var methdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Methane', data[0] || 0]  // Set to 0 if data is null or undefined
    ]);
    
    var carbondata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['CO', data[1] || 0]
    ]);

    var aqdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Air Quality', data[2] || 0]
    ]);

    var butdata = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Butane', data[3] || 0]
    ]);

    // Redraw the gauges with updated data
    var methguage = new google.visualization.Gauge(document.getElementById('methaneGauge'));
    var carbguage = new google.visualization.Gauge(document.getElementById('carbonGauge'));
    var aqguage = new google.visualization.Gauge(document.getElementById('aqGauge'));
    var butguage = new google.visualization.Gauge(document.getElementById('butaneGauge'));

    methguage.draw(methdata, methoptions);
    carbguage.draw(carbondata, carboptions);
    aqguage.draw(aqdata, aqoptions);
    butguage.draw(butdata, butoptions);
}

setInterval(sendGuageUpdate, 5000);
