from flask import Flask, render_template, redirect, jsonify, request
import subprocess

from services.measurements import get_history
from services.status import get_status
from services.settings import get_setting

app = Flask(__name__)


@app.route("/")
def index():

    status = get_status()

    return render_template(
        "index.html",
        level_cm=status["level_cm"],
        pump_state=status["pump_state"],
        auto_mode=status["auto_mode"],
        remaining_seconds=status["remaining_seconds"]
    )


@app.route("/history")
def history():

    return jsonify(
        get_history(
            request.args.get("range", "24h")
        )
    )


@app.route("/status")
def status():

    return jsonify(
        get_status()
    )


@app.route("/pump/toggle")
def pump_toggle():

    state = get_setting(
        "pump_state",
        "OFF"
    )

    if state == "ON":

        subprocess.run(
            [
                "python3",
                "/home/mike5d/pump.py",
                "off"
            ]
        )

    else:

        subprocess.run(
            [
                "python3",
                "/home/mike5d/pump.py",
                "on"
            ]
        )

    return jsonify({"success": True})


@app.route("/auto/toggle")
def auto_toggle():

    from services.settings import (
        set_setting
    )

    current = get_setting(
        "auto_mode",
        "0"
    )

    set_setting(
        "auto_mode",
        "1" if current == "0" else "0"
    )

    return redirect("/")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
