function getGraphData(){
    $.post("/getChartData", {}, function(data){
        updateChart(data);
    });
}

function getGraphData24(){
  
    $.post("/getChartData_24", {}, function(data){
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

    let carbonData = data.carbon.value.map((value) => value === null ? 0 : value);
    let methaneData = data.methane.value.map((value) => value === null ? 0 : value);
    let airqData = data.airq.value.map((value) => value === null ? 0 : value);
    let butaneData = data.butane.value.map((value) => value === null ? 0 : value);
    
    charts['carbon'].data.datasets[0].data = carbonData;
    charts['carbon'].data.labels = data.carbon.timestamp;
    charts['carbon'].update();

    charts['methane'].data.datasets[0].data = methaneData;
    charts['methane'].data.labels = data.methane.timestamp;
    charts['methane'].update();

    charts['airq'].data.datasets[0].data = airqData;
    charts['airq'].data.labels = data.airq.timestamp;
    charts['airq'].update();

    charts['butane'].data.datasets[0].data = butaneData;
    charts['butane'].data.labels = data.butane.timestamp;
    charts['butane'].update();
}

function updateChart24(data){
    var datas = data;
    console.log(datas);

    let carbonData = data.carbon.value.map((value) => value === null ? 0 : value);
    let methaneData = data.methane.value.map((value) => value === null ? 0 : value);
    let airqData = data.airq.value.map((value) => value === null ? 0 : value);
    let butaneData = data.butane.value.map((value) => value === null ? 0 : value);
    
    charts24['carbon'].data.datasets[0].data = carbonData;
    charts24['carbon'].data.labels = data.carbon.timestamp;
    charts24['carbon'].update();

    charts24['methane'].data.datasets[0].data = methaneData;
    charts24['methane'].data.labels = data.methane.timestamp;
    charts24['methane'].update();

    charts24['airq'].data.datasets[0].data = airqData;
    charts24['airq'].data.labels = data.airq.timestamp;
    charts24['airq'].update();

    charts24['butane'].data.datasets[0].data = butaneData;
    charts24['butane'].data.labels = data.butane.timestamp;
    charts24['butane'].update();
}

getGraphData();
getGraphData24();

setInterval(getGraphData, 5000);
setInterval(getGraphData24, 20000);