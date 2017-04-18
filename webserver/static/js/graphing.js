//var socket = io("http://10.104.84.214")
var socket = io("localhost:5000")

socket.on('connect', function() {
    console.log("Talking with server!");
})

Chart.defaults.global.maintainAspectRatio = false;
Chart.defaults.global.legend.display = false;
Chart.defaults.global.tooltips.enabled = true;

function createGraph(name) {
    return new Chart(name, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '',
                data: [],
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
                        },
                    },
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10
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
}

function addData(chart, data, label) {
    chart.data.labels.push(moment(label));
    chart.data.datasets[0].data.push(data);
    chart.update(50, true);
}

function scaleSeconds(chart) {
    chart.options.scales.xAxes[0].time.unit = 'second';
    chart.options.scales.xAxes[0].time.round = 'second';
    chart.options.scales.xAxes[0].time.displayFormats = {second: 'hh:mm:ss a'}
    chart.update(50, true);
}

function scaleMinutes(chart) {
    chart.options.scales.xAxes[0].time.unit = 'second';
    chart.options.scales.xAxes[0].time.round = 'second';
    chart.options.scales.xAxes[0].time.displayFormats = {second: 'hh:mm a'}
    chart.update(50, true);
}

function scaleHours(chart) {
    chart.options.scales.xAxes[0].time.unit = 'second';
    chart.options.scales.xAxes[0].time.round = 'second';
    chart.options.scales.xAxes[0].time.displayFormats = {second: 'hh a'}
    chart.update(50, true);
}

function lastMinute(chart) {
    chart.options.scales.xAxes[0].time.min = moment().subtract(1, 'minutes');
    scaleSeconds(chart)
}

function lastHour(chart) {
    chart.options.scales.xAxes[0].time.min = moment().subtract(1, 'hours');
    scaleMinutes(chart)
}

function lastTwelveHours(chart) {
    chart.options.scales.xAxes[0].time.min = moment().subtract(12, 'hours');
    scaleHours(chart);
}

function lastDay(chart) {
    chart.options.scales.xAxes[0].time.min = moment().subtract(1, 'days');
    scaleHours(chart);
}

function dataListen(chart) {
    console.log(name)
    socket.on('temp-data', function(data) {
        addData(chart, data.data, (new Date()).getTime());
        lastMinute(chart);
        $('#temp-display').html(data.data);
    });

    socket.on('occ-data', function(data) {
        addData(chart, data.data, (new Date()).getTime());
        lastMinute(chart);
        $('#occ-display').html(data.data);
    });

    socket.on('gas-data', function(data) {
        addData(chart, data.data, (new Date()).getTime());
        lastMinute(chart);
        $('#temp-display').html(data.data);
    });

    socket.on('temp-data-dump', function(data) {
        var temps = [];
        var labels = [];

        for(var key in data) {
            if(data.hasOwnProperty(key)) {
                console.log(moment(data[key.time]));
                temps.push(data[key].data);
                labels.push(moment(data[key.time]));
            }
        }

        chart.data.labels = labels;
        chart.data.datasets[0].data = temps;
        chart.update(50, true);
    });

    //socket.emit('request-temp-data', {'id': 'xyz'})
}