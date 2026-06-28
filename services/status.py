from datetime import datetime

from services.settings import get_setting
from services.measurements import get_last_level_cm


def get_status():

    pump_state = get_setting("pump_state", "OFF")
    auto_mode = get_setting("auto_mode", "0")
    deadline = get_setting("pump_off_deadline", "")

    remaining_seconds = 0

    if deadline and pump_state == "ON":

        try:

            deadline_dt = datetime.strptime(
                deadline,
                "%Y-%m-%d %H:%M:%S"
            )

            remaining_seconds = max(
                0,
                int(
                    (deadline_dt - datetime.now()).total_seconds()
                )
            )

        except Exception:
            remaining_seconds = 0

    return {
        "level_cm": get_last_level_cm(),
        "pump_state": pump_state,
        "auto_mode": auto_mode,
        "remaining_seconds": remaining_seconds
    }
