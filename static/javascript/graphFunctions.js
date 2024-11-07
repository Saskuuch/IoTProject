function getGraphData(){
    $.post("http://127.0.0.1:2300/getChartData", {}, function(data){
        updateChart(data);
    });
}

function getGraphData24(){
    $.post("http://127.0.0.1:2300/getChartData_24", {}, function(data){
        updateChart24(data);
    });
}

var carbctx = document.getElementById("carbonGraph_1h").getContext("2d");
var methctx = document.getElementById("methaneGraph_1h").getContext("2d");
var aqctx = document.getElementById("aqGraph_1h").getContext("2d");
var butctx = document.getElementById("butaneGraph_1h").getContext("2d");

var carbctx24 = document.getElementById("carbonGraph_24h").getContext("2d");
var methctx24 = document.getElementById("methaneGraph_24h").getContext("2d");
var aqctx24 = document.getElementById("aqGraph_24h").getContext("2d");
var butctx24 = document.getElementById("butaneGraph_24h").getContext("2d");

var chartOptions = {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "1-Hour PPM",
        data: [],
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        xAxes: [{
          type: "time",
          time: {
            unit: "minute",
            unitStepSize: 5,
            displayFormats: {
              minute: "hh:mm",
              hour: "hhA"
            },
            tooltipFormat: "hh:mm:ss"
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            stepSize: 5,
            font: {
              size: 12
            }
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            font: {
              size: 12
            }
          }
        }]
      },
      legend: {
        labels: {
          font: {
            size: 14
          }
        }
      }
    }
  };
  var chartOptions24 = {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "24-Hour PPM",
        data: [],
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        xAxes: [{
          type: "time",
          time: {
            unit: "minute",
            unitStepSize: 5,
            displayFormats: {
              minute: "hh:mm",
              hour: "hhA"
            },
            tooltipFormat: "hh:mm:ss"
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            stepSize: 5,
            font: {
              size: 12
            }
          }
        }],
        yAxes: [{
          ticks: {
            beginAtZero: true,
            font: {
              size: 12
            }
          }
        }]
      },
      legend: {
        labels: {
          font: {
            size: 14
          }
        }
      }
    }
  };
  

    var charts = {"carbon" : new Chart(carbctx, chartOptions), 
        "methane" : new Chart(methctx, chartOptions), "airq" : new Chart(aqctx, chartOptions), "butane" : new Chart(butctx, chartOptions)};
    var charts24 = {"carbon" : new Chart(carbctx24, chartOptions24), 
        "methane" : new Chart(methctx24, chartOptions24), "airq" : new Chart(aqctx24, chartOptions24), "butane" : new Chart(butctx24, chartOptions24)};

function updateChart(data){
    var datas = data;
    console.log(datas);
    
    charts['carbon'].data.datasets[0].data = data.carbon.map((d) => d.value);
    charts['carbon'].data.labels = data.carbon.map((d) => d.timestamp);
    charts['carbon'].update();
    
    charts['methane'].data.datasets[0].data = data.methane.map((d) => d.value);
    charts['methane'].data.labels = data.methane.map((d) => d.timestamp);
    charts['methane'].update();
    
    charts['airq'].data.datasets[0].data = data.airq.map((d) => d.value);
    charts['airq'].data.labels = data.airq.map((d) => d.timestamp);
    charts['airq'].update();
    
    charts['butane'].data.datasets[0].data = data.butane.map((d) => d.value);
    charts['butane'].data.labels = data.butane.map((d) => d.timestamp);
    charts['butane'].update();
}

function updateChart24(data){
    var datas = data;
    console.log(datas);
    
    charts24['carbon'].data.datasets[0].data = data.carbon.map((d) => d.value);
    charts24['carbon'].data.labels = data.carbon.map((d) => d.timestamp);
    charts24['carbon'].update();
    
    charts24['methane'].data.datasets[0].data = data.methane.map((d) => d.value);
    charts24['methane'].data.labels = data.methane.map((d) => d.timestamp);
    charts24['methane'].update();
    
    charts24['airq'].data.datasets[0].data = data.airq.map((d) => d.value);
    charts24['airq'].data.labels = data.airq.map((d) => d.timestamp);
    charts24['airq'].update();
    
    charts24['butane'].data.datasets[0].data = data.butane.map((d) => d.value);
    charts24['butane'].data.labels = data.butane.map((d) => d.timestamp);
    charts24['butane'].update();
}

getGraphData();
getGraphData24();

setInterval(getGraphData, 5000);
setInterval(getGraphData24, 20000);