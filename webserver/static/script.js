var socket = io.connect('http://' + document.domain);
socket.on('push', function(data) {
    pushData(data.num);
});

function newDate(days) {
    return moment().add(days, 'h').toDate();
}

var counter = -9
function pushData(num) {
    if(data.length > 24) {
        data.shift();
        labels.shift();
    }
    labels.push(newDate(counter++));
    data.push(num);
    chart.update(50, true);
}

var ctx = "graph1"

Chart.defaults.global.maintainAspectRatio = false;
Chart.defaults.global.legend.display = false;
Chart.defaults.global.tooltips.enabled = true;

var labels = [newDate(-12), newDate(-11), newDate(-10)];
var data = [72, 75, 73];

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: '',
            data: data,
            borderColor: "rgba(220,20,20,1)",
            backgroundColor: "rgba(220,20,20,0.5)"
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: "time",
                time: {
                    unit: 'hour',
                    round: 'hour',
                    displayFormats: {
                        hour: 'hh a'
                    }
                },
                ticks: {
                    'autoskip': true
                }
            }],
            yAxes: [{
                ticks: {
                    suggestedMin: 65,
                    suggestedMax: 80
                }
            }]
        }
    }
});