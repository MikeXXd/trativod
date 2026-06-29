let remaining = 0;

let lastLevel = null;

async function refreshStatus() {

    try {

        const response = await fetch("/status");

        if (!response.ok) {
            return;
        }

        const status = await response.json();

        remaining = status.remaining_seconds;

        const level = document.getElementById("levelValue");

        if (level) {

            level.textContent = status.level_cm + " cm";

        }

        if (
            lastLevel !== null &&
            lastLevel !== status.level_cm
        ) {

            refreshChart();

        }

        lastLevel = status.level_cm;

        const pumpStatus = document.getElementById("pumpStatus");

        if (pumpStatus) {

            pumpStatus.textContent =
                status.pump_state === "ON"
                    ? "🔴 ZAPNUTO"
                    : "🟢 VYPNUTO";

        }

        const autoStatus = document.getElementById("autoStatus");

        if (autoStatus) {

            autoStatus.textContent =
                status.auto_mode === "1"
                    ? "🟢 AUTO"
                    : "⚪ MANUAL";

        }

    } catch (err) {

        console.error(err);

    }

}

async function togglePump(event) {

    event.preventDefault();

    const response = await fetch("/pump/toggle");

    if (!response.ok) {
        return;
    }

    await refreshStatus();

}

function startStatusRefresh() {

    refreshStatus();

    setInterval(refreshStatus, 10000);

    const button =
        document.getElementById("pumpButton");

    if (button) {

        button.addEventListener(
            "click",
            togglePump
        );

    }

}
