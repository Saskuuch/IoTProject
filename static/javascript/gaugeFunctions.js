google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);
function drawChart() {

var methdata = google.visualization.arrayToDataTable([
['Label', 'Value'],
['Methane', 102]
]);
var methoptions = {
min:0, max:10000,
width: 400, height: 140,
redFrom: 8000, redTo: 10000,
yellowFrom:1000, yellowTo: 8000,
minorTicks: 20
};
var carbondata = google.visualization.arrayToDataTable([
['Label', 'Value'],
['CO', 5]

]);
var carboptions = {
min:0, max:1000,
width: 400, height: 140,
redFrom: 500, redTo: 1000,
yellowFrom:50, yellowTo: 500,
minorTicks: 20
};
var aqdata = google.visualization.arrayToDataTable([
['Label', 'Value'],
['Air Quality', 22]
]);
var aqoptions = {
min:0, max:1000,
width: 400, height: 140,
redFrom: 700, redTo: 1000,
yellowFrom:200, yellowTo: 700,
minorTicks: 20
};
var butdata = google.visualization.arrayToDataTable([
['Label', 'Value'],
['Butane', 33]
]);

var butoptions = {
min:0, max:1600,
width: 400, height: 140,
redFrom: 1000, redTo: 1600,
yellowFrom:700, yellowTo: 1000,
minorTicks: 30
};

var methguage = new google.visualization.Gauge(document.getElementById('methaneGauge'));
var carbguage = new google.visualization.Gauge(document.getElementById('carbonGauge'));
var aqguage = new google.visualization.Gauge(document.getElementById('aqGauge'));
var butguage = new google.visualization.Gauge(document.getElementById('butaneGauge'));

methguage.draw(methdata, methoptions);
carbguage.draw(carbondata, carboptions);
aqguage.draw(aqdata, aqoptions);
butguage.draw(butdata, butoptions);
}