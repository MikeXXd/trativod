let chart = null;

let currentRange = "24h";

function updateActiveButton() {

    document
        .querySelectorAll(".range-button")
        .forEach(button => {

            button.classList.toggle(
                "active",
                button.dataset.range === currentRange
            );

        });

}

function getTickLimit() {

    switch (currentRange) {

        case "1h":
            return 6;

        case "24h":
            return 12;

        case "3d":
            return 12;

        case "1w":
            return 7;

        case "1m":
            return 10;

        default:
            return 10;

    }

}

async function loadHistory(range = currentRange) {

    currentRange = range;

    localStorage.setItem("historyRange", range);

    updateActiveButton();

    const response = await fetch("/history?range=" + range);

    const data = await response.json();

    const labels = data.map(p => p.time);

    const values = data.map(p => p.level);

    if (!chart) {

        const ctx = document.getElementById("historyChart");

        chart = new Chart(ctx, {

            type: "line",

            data: {

                labels,

                datasets: [{

                    label: "Hladina (cm)",

                    data: values,

                    tension: 0.2,

                    pointRadius: 0

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: true,

                animation: false,

                scales: {

                    x: {

                        ticks: {

                            maxTicksLimit: getTickLimit()

                        }

                    },

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

        chart.options.scales.x.ticks.maxTicksLimit =
            getTickLimit();

        chart.update("none");

    }

}

async function refreshChart() {

    if (!chart) {
        return;
    }

    await loadHistory(currentRange);

}

document.addEventListener("DOMContentLoaded", () => {

    currentRange =
        localStorage.getItem("historyRange") || "24h";

    updateActiveButton();

});
