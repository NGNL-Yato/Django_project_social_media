        
        var acc = document.getElementsByClassName("tabButton");
        var i;

        for (i = 0; i < acc.length; i++) {
            acc[i].addEventListener("click", function(e) {
                var target = e.target;
                var panel = target.parentElement.getElementsByClassName('panel')[0]
                console.log(panel);
                panel.style.height = null;
                console.log(target);
            });
        }

var arr = [10, 1, 1, 3, 2, 10, 7, 9, 2, 5, 3, 9, 8, 4, 3, 0];
        var backgroundColors = [];
        arr.forEach(v => backgroundColors.push("rgba(64, 80, 245, " + v / 10 + ")"))

        var data = {
            labels: ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"],
            datasets: [{
                label: 'A',
                backgroundColor: backgroundColors,
                data: arr,
            }]
        };

        var options = {
            responsive: true,
            cornerRadius: 0,
            maintainAspectRatio: false,
            legend: {
                display: false,
                position: 'bottom',
            },
            scales: {
                yAxes: [{
                    display: false,
                    gridLines: {
                        display: false,
                    },
                    ticks: {
                        maxTicksLimit: 5,
                    }
                }],
                xAxes: [{
                    display: true,
                    barPercentage: 1,
                    gridLines: {
                        display: false,
                    },
                    ticks: {
                        userCallback: function(item, index) {
                            if (!(index % 3)) return item;
                        },
                        fontColor: '#9c9eb2'
                    }
                }]
            }
        };


        var ctx = document.getElementById('activityChart1').getContext('2d');
        var ctx2 = document.getElementById('activityChart2').getContext('2d');
        var ctx3 = document.getElementById('activityChart3').getContext('2d');
        var ctx4 = document.getElementById('activityChart4').getContext('2d');
        var ctx5 = document.getElementById('activityChart5').getContext('2d');
        var ctx6 = document.getElementById('activityChart6').getContext('2d');
        var myLineChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: options
        });
        var myLineChart = new Chart(ctx2, {
            type: 'bar',
            data: data,
            options: options
        });
        var myLineChart = new Chart(ctx3, {
            type: 'bar',
            data: data,
            options: options
        });
        var myLineChart = new Chart(ctx4, {
            type: 'bar',
            data: data,
            options: options
        });
        var myLineChart = new Chart(ctx5, {
            type: 'bar',
            data: data,
            options: options
        });
        var myLineChart = new Chart(ctx6, {
            type: 'bar',
            data: data,
            options: options
        });

document.getElementById('closeAlert').addEventListener('click', closeAlert, {
            once: true
        });

        function closeAlert() {
            document.getElementsByClassName('upgradeAccount')[0].style.display = "none";
        }