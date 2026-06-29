document.addEventListener("DOMContentLoaded", () => {

    const savedRange =
        localStorage.getItem("historyRange") || "24h";

    loadHistory(savedRange);

    startStatusRefresh();

    startCountdown();

});
