import random
import time
import subprocess
from datetime import datetime, timedelta

def run_updater():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running updater...")
    subprocess.run(["python3", "auto_updater/updater.py"])

def main():
    # Определяем, сколько запусков будет сегодня
    runs = random.choices([0, 1, 2], weights=[1, 3, 2])[0]
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Planned {runs} run(s) for today")

    if runs == 0:
        return

    # Диапазон времени: 09:00 - 22:00
    start_sec = 9 * 3600
    end_sec = 22 * 3600

    # Выбираем случайные времена (в секундах от начала дня)
    run_times = sorted(random.sample(range(start_sec, end_sec), runs))

    for t in run_times:
        now = datetime.now()
        target = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=t)
        wait_sec = (target - now).total_seconds()

        if wait_sec > 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Waiting {int(wait_sec)} sec until {target.strftime('%H:%M:%S')}")
            time.sleep(wait_sec)

        run_updater()

if __name__ == "__main__":
    main()
