#TODO #1 Make a label housing timer
#TODO #2 Put an image of a tomato at the center of the window
#TODO #3 Make the image clickable and have it pause or start the timer
#TODO #4 Add increment button to increase current timer by 1 min
#TODO #5 Have a sound ring out when timer hits 0
#TODO #6 Replace the image with a GIF of it turning big and then small back again when timer hits 0
#TODO #7 Make a field to set the maximum timer and make it so that it does not affect running or paused timer
#TODO #8 Make a stop button
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

        self.stop_button = tk.Button(self.master)
        
        self.time_left = 25*60
        self.timer_running = False

        self.timer_entry = tk.Entry(self.master)
        self.timer_entry.pack(pady=10)

        self.set_timer_button = tk.Button(self.master, text="Set Timer", command=self.set_timer)
        self.set_timer_button.pack(pady=10)

    def set_timer(self):
        try:
            self.time_left = int(self.timer_entry.get().split(":")[0])*60 + int(self.timer_entry.get().split(":")[1])
            self.timer_label.config(text=f"{self.time_left//60:02d}:{self.time_left%60:02d}")
        except ValueError:
            pass

    def start_timer(self):
        if not self.timer_running:
            self.timer_label.config(text=f"{self.time_left:02d}:00")
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            time_string = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
        if self.time_left > 0:
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.timer_label.config(text="Time's up!")

root = tk.Tk()
app = TimerApp(root)
root.mainloop()