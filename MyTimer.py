import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread
import winsound


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("デスクトップタイマー")

        # タイマー設定
        self.work_time = 25  # 作業時間（分）
        self.break_time = 5  # 休憩時間（分）
        self.is_running = False
        self.start_time = None
        self.last_break_start = None
        self.completed_breaks = 0  # 完全に終了した休憩の回数

        # ラベル
        self.label = tk.Label(root, text="タイマー設定", font=("Arial", 16))
        self.label.pack(pady=10)

        # 作業時間入力
        tk.Label(root, text="作業時間 (分):").pack()
        self.work_entry = tk.Entry(root)
        self.work_entry.insert(0, str(self.work_time))
        self.work_entry.pack()

        # 休憩時間入力
        tk.Label(root, text="休憩時間 (分):").pack()
        self.break_entry = tk.Entry(root)
        self.break_entry.insert(0, str(self.break_time))
        self.break_entry.pack()

        # ボタン
        self.start_button = tk.Button(root, text="開始", command=self.toggle_timer, bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="リセット", command=self.reset_timer, bg="blue", fg="white")
        self.reset_button.pack(pady=5)

        # 状態表示
        self.status_label = tk.Label(root, text="停止中", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # 作業時間と休憩時間の表示
        self.work_time_label = tk.Label(root, text="作業時間: 0 分", font=("Arial", 12))
        self.work_time_label.pack(pady=5)
        self.break_time_label = tk.Label(root, text="休憩時間: 0 分", font=("Arial", 12))
        self.break_time_label.pack(pady=5)

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="開始", bg="green")
            self.status_label.config(text="停止中")
            self.update_displayed_times()
        else:
            self.is_running = True
            self.start_button.config(text="停止", bg="red")
            self.status_label.config(text="作業中")
            self.start_time = time.time()
            self.last_break_start = None
            self.completed_breaks = 0
            try:
                self.work_time = int(self.work_entry.get())
                self.break_time = int(self.break_entry.get())
            except ValueError:
                messagebox.showerror("エラー", "作業時間と休憩時間は数字で入力してください。")
                self.is_running = False
                return
            Thread(target=self.run_timer, daemon=True).start()

    def reset_timer(self):
        self.is_running = False
        self.start_button.config(text="開始", bg="green")
        self.status_label.config(text="停止中")
        self.start_time = None
        self.last_break_start = None
        self.completed_breaks = 0
        self.work_time_label.config(text="作業時間: 0 分")
        self.break_time_label.config(text="休憩時間: 0 分")

    def run_timer(self):
        while self.is_running:
            # 作業時間
            self.status_label.config(text="作業中")
            for _ in range(self.work_time * 60):
                if not self.is_running:
                    self.update_displayed_times()
                    return
                time.sleep(1)

            self.play_sound()
            self.completed_breaks += 1
            self.last_break_start = time.time()

            # 休憩時間
            self.status_label.config(text="休憩中")
            for _ in range(self.break_time * 60):
                if not self.is_running:
                    self.update_displayed_times()
                    return
                time.sleep(1)

            self.play_sound()
            self.last_break_start = None

    def update_displayed_times(self):
        if self.start_time is None:
            return

        current_time = time.time()
        elapsed_time = (current_time - self.start_time) / 60  # 分に変換

        # 休憩時間と作業時間の計算
        if self.completed_breaks == 0 and self.last_break_start is None:
            # 最初の休憩開始前に停止
            work_time = elapsed_time
            break_time = 0
        elif self.completed_breaks > 0 and self.last_break_start is None:
            # 休憩終了後、作業時間中に停止
            break_time = self.break_time * self.completed_breaks
            work_time = elapsed_time - break_time
        elif self.completed_breaks > 0 and self.last_break_start is not None:
            # 休憩途中で停止
            break_elapsed = (current_time - self.last_break_start) / 60
            break_time = self.break_time * (self.completed_breaks - 1) + break_elapsed
            work_time = elapsed_time - break_time
        else:
            work_time = elapsed_time
            break_time = 0

        # ラベル更新
        self.work_time_label.config(text=f"作業時間: {work_time:.2f} 分")
        self.break_time_label.config(text=f"休憩時間: {break_time:.2f} 分")

    def play_sound(self):
        try:
            winsound.Beep(440, 1000)  # 440Hzで1秒間のビープ音
        except Exception as e:
            print(f"音の再生エラー: {e}")


# GUIの起動
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
