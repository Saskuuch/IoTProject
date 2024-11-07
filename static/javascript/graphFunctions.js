function getGraphData(){
    $.post("http://127.0.0.1:8000/getChartData", {}, function(data){
        updateChart(data);
    });
}

var carbctx = document.getElementById("carbonGraph").getContext("2d");
var methctx = document.getElementById("methaneGraph").getContext("2d");
var aqctx = document.getElementById("aqGraph").getContext("2d");
var butctx = document.getElementById("butaneGraph").getContext("2d");

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

var charts = {"carbon" : new Chart(carbctx, chartOptions), 
    "methane" : new Chart(methctx, chartOptions), "airq" : new Chart(aqctx, chartOptions), "butane" : new Chart(butctx, chartOptions)};

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

    // Object.keys(charts).forEach((type) => {
    //     charts[type].update();
    // });
}

getGraphData();

setInterval(getGraphData, 5000);