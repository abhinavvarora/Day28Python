import tkinter as tk
import threading
import playsound
import pandas
import random
from PIL import Image, ImageTk
import textwrap

class TimerApp:
    def __init__(self, master):
        self.master = master
        # self.master.geometry("1200x500")
        # self.master.resizable(False, False)
        self.master.title("Pomodoro")
        
        self.df = pandas.read_excel("data/Motivational Quotes Database.xlsx")
        self.shown_before = []
        
        self.motivation_label = tk.Label(self.master)
        self.change_quote()
        self.motivation_label.grid(column=2, row=2)
        
        self.timer_type = "Work"
        self.timer_type_label = tk.Label(self.master, text=self.timer_type)
        self.timer_type_label.grid(column=2, row=3)
        
        self.tomato_photo = ImageTk.PhotoImage(Image.open("images/tomato.png").resize((300, 300)))
        self.tomato = tk.Label(self.master, image=self.tomato_photo)
        self.tomato.grid(column=2, row=4)
        
        self.timer_label = tk.Label(self.master, text="25:00", font=("Arial", 24))
        self.timer_label.grid(column=2, row=4)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.grid(column=1, row=5)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer)
        self.pause_button.grid(column=2, row=5)
        
        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer)
        self.stop_button.grid(column=3, row=5)

        self.work_max_minutes = 25
        self.work_max_seconds = 0
        self.minutes = 0
        self.seconds = 0
        self.break_max_minutes = 5
        self.break_max_seconds = 0
                
        self.time_left = self.work_max_minutes*60 + self.work_max_seconds
        self.timer_running = False
        self.timer_paused = False
        
        self.timer_entry_label = tk.Label(text="Enter timer length")
        self.timer_entry_label.grid(column=1, row=6)

        self.timer_entry = tk.Entry(self.master)
        self.timer_entry.grid(column=2, row=6)

        self.set_timer_button = tk.Button(self.master, text="Set Timer", command=self.set_timer)
        self.set_timer_button.grid(column=3, row=6)
        
    def change_quote(self):
        rand_num = random.randint(5, 45579)
        if rand_num in self.shown_before:
            self.change_quote()
        self.shown_before.append(rand_num)
        quote, author, category = self.df.iloc[rand_num]
        full_text=quote.strip(".") + " - " + author
        max_width = 100
        lines = textwrap.wrap(full_text, width = max_width)
        self.motivation_label.config(text="\n".join(lines))
        
    def play_sound(self, sound_path):
        playsound.playsound(sound_path)
        
    def set_timer(self):
        try:
            max_timer_list = self.timer_entry.get().split(":")
            self.minutes = int(max_timer_list[0])
            self.seconds = int(max_timer_list[1])
            self.time_left = self.minutes*60 + self.seconds
            self.timer_label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")
        except ValueError:
            pass
    
    def stop_timer(self):
        self.timer_running = False
        self.timer_paused = True
        self.time_left = self.minutes*60 + self.seconds
        self.timer_label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")
        
    def start_timer(self):
        if self.timer_running:
            pass
        else:
            self.timer_running = True
            self.timer_paused = False
            self.update_timer()
        
    def pause_timer(self):
        self.timer_paused = True

    def update_timer(self):
        if self.timer_running and not self.timer_paused:
            self.minutes = self.time_left // 60
            self.seconds = self.time_left % 60
            time_string = f"{self.minutes:02d}:{self.seconds:02d}"
            self.timer_label.config(text=time_string)
        if self.time_left > 0 and not self.timer_paused:
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.change_quote()
            self.timer_running = False
            time_string = f"{self.minutes:02d}:{self.seconds:02d}"
            self.timer_label.config(text=time_string)
            if self.timer_type == "Work":
                self.timer_type = "Break"
                self.minutes = self.break_max_minutes
                self.seconds = self.break_max_seconds
                sound_thread = threading.Thread(target=self.play_sound, args=("sounds/break_bell.wav", ))
                sound_thread.start()
            else:
                self.timer_type = "Work"
                self.minutes = self.work_max_minutes
                self.seconds = self.work_max_seconds
                sound_thread = threading.Thread(target=self.play_sound, args=("sounds/work_bell.wav", ))
                sound_thread.start()
            self.time_left = self.minutes*60 + self.seconds
            self.timer_label.config(text=f"{self.minutes:02d}:{self.seconds:02d}")
            self.timer_type_label.config(text=self.timer_type)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
