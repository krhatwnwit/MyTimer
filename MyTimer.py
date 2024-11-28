import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread
import winsound  # Windows用。Mac/Linuxは`playsound`を使用

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("デスクトップタイマー")

        # 初期値
        self.work_time = 25  # 作業時間（分）
        self.break_time = 5  # 休憩時間（分）
        self.is_running = False
        self.total_work_time = 0
        self.start_time = None

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

        self.reset_button = tk.Button(root, text="作業時間リセット", command=self.reset_work_time, bg="blue", fg="white")
        self.reset_button.pack(pady=5)

        # 状態表示
        self.status_label = tk.Label(root, text="停止中", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # 作業時間合計表示
        self.total_label = tk.Label(root, text="累計作業時間: 0 分", font=("Arial", 12))
        self.total_label.pack(pady=10)

    def toggle_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(text="開始", bg="green")
            self.status_label.config(text="停止中")
            self.update_total_work_time()
        else:
            self.is_running = True
            self.start_button.config(text="停止", bg="red")
            self.status_label.config(text="作業中")
            self.start_time = time.time()
            try:
                self.work_time = int(self.work_entry.get())
                self.break_time = int(self.break_entry.get())
            except ValueError:
                messagebox.showerror("エラー", "作業時間と休憩時間は数字で入力してください。")
                self.is_running = False
                return
            Thread(target=self.run_timer, daemon=True).start()

    def reset_work_time(self):
        self.total_work_time = 0
        self.total_label.config(text="累計作業時間: 0 分")

    def run_timer(self):
        while self.is_running:
            # 作業時間
            for _ in range(self.work_time * 60):
                if not self.is_running:
                    return
                time.sleep(1)
            self.play_sound()
            self.update_total_work_time()

            # 休憩時間
            self.status_label.config(text="休憩中")
            for _ in range(self.break_time * 60):
                if not self.is_running:
                    return
                time.sleep(1)
            self.play_sound()
            self.status_label.config(text="作業中")

    def update_total_work_time(self):
        if self.start_time:
            elapsed_time = (time.time() - self.start_time) / 60
            effective_time = max(0, elapsed_time - self.break_time)
            self.total_work_time += round(effective_time, 2)
            self.total_label.config(text=f"累計作業時間: {self.total_work_time:.2f} 分")

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
