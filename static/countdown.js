function startCountdown() {

    setInterval(() => {

        const button = document.getElementById("pumpButton");

        if (!button) {
            return;
        }

        if (remaining <= 0) {

            button.textContent = "Zapnout čerpadlo";

            return;
        }

        const m = Math.floor(remaining / 60);
        const s = remaining % 60;

        button.textContent =
            `Vypnout (${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")})`;

        remaining--;

    }, 1000);

}
