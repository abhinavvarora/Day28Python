#TODO #1 Make a label housing timer
#TODO 1st Done
#TODO #2 Put an image of a tomato at the center of the window
#TODO #3 Make the image clickable and have it pause or start the timer
#TODO #4 Add increment button to increase current timer by 1 min
#TODO 4th Deprecated
#TODO #5 Have a sound ring out when timer hits 0
#TODO #6 Replace the image with a GIF of it turning big and then small back again when timer hits 0
#TODO #7 Make a field to set the maximum timer
#TODO 7th Done
#TODO #8 Make a stop button
#TODO 8th Done
#TODO #9 Draw from a txt file motivational messages, display them above the pomodo tomato and change them periodically

import tkinter as tk

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Timer App")
        self.timer_label = tk.Label(self.master, text="25:00", font=("Arial", 24))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_timer)
        self.stop_button.pack(pady=20)
        
        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_timer)
        self.pause_button.pack(pady=20)
        
        self.max_minutes = 25
        self.max_seconds = 0
        self.minutes = 0
        self.seconds = 0
                
        self.time_left = self.max_minutes*60 + self.max_seconds
        self.timer_running = False
        self.timer_paused = False

        self.timer_entry = tk.Entry(self.master)
        self.timer_entry.pack(pady=10)

        self.set_timer_button = tk.Button(self.master, text="Set Timer", command=self.set_timer)
        self.set_timer_button.pack(pady=10)

    def set_timer(self):
        try:
            self.max_minutes = self.minutes = int(self.timer_entry.get().split(":")[0])
            self.max_seconds = self.seconds = int(self.timer_entry.get().split(":")[1])
            self.time_left = self.minutes*60 + self.seconds
        except ValueError:
            pass
    
    def stop_timer(self):
        self.minutes = 0
        self.seconds = 0
        self.time_left = 0
        self.timer_running = False
        self.timer_paused = False
        
    def start_timer(self):
        if self.time_left == 0:
            self.minutes = self.max_minutes
            self.seconds = self.max_seconds
            self.time_left = self.max_minutes*60 + self.max_seconds
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
            self.timer_running = False
            time_string = f"{self.minutes:02d}:{self.seconds:02d}"
            self.timer_label.config(text=time_string)

root = tk.Tk()
app = TimerApp(root)
root.mainloop()
