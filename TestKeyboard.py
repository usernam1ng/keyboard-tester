import time
import numpy as np
from pynput import keyboard

class PollingRateTester:
    def __init__(self):
        self.intervals = []       # интервалы в секундах
        self.last_time = None
        self.event_count = 0

    def on_press(self, key):
        # Выход по ESC
        if key == keyboard.Key.esc:
            print("\n[Выход]")
            return False

        now = time.perf_counter()

        if self.last_time is not None:
            interval = now - self.last_time
            freq = 1.0 / interval if interval > 0 else 0
            self.intervals.append(interval)
            self.event_count += 1
            print(f"Нажатие #{self.event_count}: {interval*1000:.2f} мс → {freq:.1f} Гц")
        else:
            print("Первое нажатие (пропускаем, нужен интервал)")

        self.last_time = now

    def run(self):
        print("Измерение частоты опроса (polling rate) клавиатуры")
        print("Нажимайте любую клавишу (кроме ESC). Для выхода нажмите ESC.\n")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        self.show_stats()

    def show_stats(self):
        if len(self.intervals) < 2:
            print("Недостаточно данных (нужно минимум 2 нажатия).")
            return

        freqs = 1.0 / np.array(self.intervals)
        avg_freq = np.mean(freqs)
        median_freq = np.median(freqs)
        min_freq = np.min(freqs)
        max_freq = np.max(freqs)
        std_freq = np.std(freqs)

        print("\n========== Статистика (Гц) ==========")
        print(f"Измеренных интервалов: {len(self.intervals)}")
        print(f"Средняя частота:       {avg_freq:.1f} Гц")
        print(f"Медианная частота:     {median_freq:.1f} Гц")
        print(f"Минимальная частота:   {min_freq:.1f} Гц")
        print(f"Максимальная частота:  {max_freq:.1f} Гц")
        print(f"Ст. отклонение:        {std_freq:.1f} Гц")
        print(f"Средний интервал:      {1000/avg_freq:.2f} мс")

        # Простая гистограмма интервалов (мс)
        intervals_ms = np.array(self.intervals) * 1000
        bins = [0, 5, 10, 15, 20, 25, 30, 40, 50, 100]
        hist, _ = np.histogram(intervals_ms, bins=bins)
        print("\nРаспределение интервалов (мс):")
        for i in range(len(bins)-1):
            if hist[i] > 0:
                bar = '█' * (hist[i] // max(1, max(hist)//40))
                print(f"  {bins[i]:3d}-{bins[i+1]:3d}: {bar} ({hist[i]})")

if __name__ == "__main__":
    tester = PollingRateTester()
    tester.run()