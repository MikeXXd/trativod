let chart = null;

let currentRange = "24h";

async function loadHistory(range = currentRange) {

    currentRange = range;

    const response = await fetch("/history?range=" + range);
    const data = await response.json();

    const labels = data.map(p => p.time);
    const values = data.map(p => p.level);

    if (!chart) {

        const ctx = document.getElementById("historyChart");

        chart = new Chart(ctx, {

            type: "line",

            data: {

                labels: labels,

                datasets: [{

                    label: "Hladina (cm)",

                    data: values,

                    tension: 0.2

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: true,

                animation: false,

                scales: {

                    y: {

                        reverse: true,

                        title: {

                            display: true,

                            text: "cm"

                        }

                    }

                }

            }

        });

    } else {

        chart.data.labels = labels;
        chart.data.datasets[0].data = values;

        chart.update("none");

    }

}
