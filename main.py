import psutil


def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return {
            "percentage": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left": battery.secsleft
        }
    else:
        return None


battery_info = get_battery_info()

if battery_info:
    print(f"Batareya foizi: {battery_info['percentage']}%")
    print(f"Elektr tarmog'iga ulangan: {battery_info['plugged_in']}")
    time_left = battery_info['time_left']
    if time_left == psutil.POWER_TIME_UNLIMITED:
        print("Tarmoqda ulangan")
    elif time_left == psutil.POWER_TIME_UNKNOWN:
        print("Qolgan vaqt noma'lum")
    else:
        hours, remainder = divmod(time_left, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Qolgan vaqt: {hours} soat, {minutes} daqiqa, {seconds} soniya")
else:
    print("Batareya haqida ma'lumot olishning imkoni bo'lmadi")
