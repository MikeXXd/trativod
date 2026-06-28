let remaining = 0;

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

function startStatusRefresh() {

    refreshStatus();

    setInterval(refreshStatus, 10000);

}
