import random
import time
import subprocess
from datetime import datetime

def run_updater():
    print(f"[{datetime.now()}] Running updater...")
    subprocess.run(["python3", "auto_updater/updater.py"])

def main():
    # случайное количество запусков на сегодня (0, 1 или 2)
    runs = random.choice([0, 1, 2])
    print(f"[{datetime.now()}] Planned {runs} runs for today")

    if runs == 0:
        return

    # допустимый диапазон (с 9:00 до 22:00)
    start_sec = 9 * 3600
    end_sec = 22 * 3600
    day_seconds = range(start_sec, end_sec)

    # выбираем случайные моменты времени (в секундах от начала дня)
    run_times = sorted(random.sample(day_seconds, runs))

    for t in run_times:
        now = datetime.now()
        target = now.replace(hour=0, minute=0, second=0, microsecond=0) + \
                 timedelta(seconds=t)
        wait_sec = (target - now).total_seconds()

        if wait_sec > 0:
            print(f"[{datetime.now()}] Waiting {int(wait_sec)} sec until {target}")
            time.sleep(wait_sec)

        run_updater()

if __name__ == "__main__":
    from datetime import timedelta
    main()
